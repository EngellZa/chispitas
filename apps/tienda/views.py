from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, F
from django.db import transaction

from apps.tienda.models import Producto, Categoria, Pedido, ItemPedido


def index(request):
    """Vista principal de la tienda"""
    categorias = Categoria.objects.filter(activo=True)
    productos = Producto.objects.filter(activo=True)

    categoria_slug = request.GET.get('categoria')
    if categoria_slug:
        productos = productos.filter(categoria__slug=categoria_slug)

    search = request.GET.get('search', '')
    if search:
        productos = productos.filter(
            Q(nombre__icontains=search) | Q(descripcion__icontains=search)
        )

    return render(request, 'tienda/index.html', {
        'categorias': categorias,
        'productos': productos,
        'categoria_actual': categoria_slug,
        'search': search,
    })


def agregar_al_carrito(request, producto_id):
    """Agregar producto al carrito"""
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    carrito = request.session.get('carrito', {})
    producto_id_str = str(producto_id)

    cantidad_actual = carrito.get(producto_id_str, {}).get('cantidad', 0)

    if cantidad_actual < producto.stock:
        carrito[producto_id_str] = {
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'cantidad': cantidad_actual + 1,
            'imagen': producto.imagen,
        }
        messages.success(request, f'¡{producto.nombre} agregado al carrito!')
    else:
        messages.warning(request, f'No hay más stock disponible de {producto.nombre}')

    request.session['carrito'] = carrito
    request.session.modified = True

    return redirect(request.META.get('HTTP_REFERER', 'index'))


def ver_carrito(request):
    """Ver carrito con stock real actualizado"""
    carrito = request.session.get('carrito', {})
    items = []
    total = 0

    # Para poder eliminar items con stock 0 sin romper el loop
    productos_a_eliminar = []

    for producto_id, item in carrito.items():
        producto = get_object_or_404(Producto, id=int(producto_id), activo=True)

        # Si no hay stock, lo quitamos del carrito
        if producto.stock <= 0:
            productos_a_eliminar.append(producto_id)
            messages.warning(request, f'{producto.nombre} ya no tiene stock y se eliminó del carrito.')
            continue

        # Si la cantidad en sesión es mayor al stock actual, ajustarla
        if item['cantidad'] > producto.stock:
            item['cantidad'] = producto.stock
            messages.warning(
                request,
                f'Se ajustó la cantidad de {producto.nombre} por cambio en stock.'
            )

        subtotal = float(producto.precio) * item['cantidad']
        total += subtotal

        items.append({
            'id': producto_id,
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'cantidad': item['cantidad'],
            'imagen': producto.imagen,
            'stock': producto.stock,
            'subtotal': subtotal,
        })

    # Eliminar los productos sin stock del carrito
    for pid in productos_a_eliminar:
        carrito.pop(pid, None)

    request.session['carrito'] = carrito
    request.session.modified = True

    return render(request, 'tienda/carrito.html', {
        'items': items,
        'total': total,
    })


def actualizar_cantidad(request, producto_id):
    """Actualizar cantidad en carrito"""
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        producto_id_str = str(producto_id)

        if producto_id_str in carrito:
            producto = get_object_or_404(Producto, id=producto_id, activo=True)
            accion = request.POST.get('accion')

            if accion == 'incrementar':
                if carrito[producto_id_str]['cantidad'] < producto.stock:
                    carrito[producto_id_str]['cantidad'] += 1
                else:
                    messages.warning(request, 'No hay más stock disponible')

            elif accion == 'decrementar':
                if carrito[producto_id_str]['cantidad'] > 1:
                    carrito[producto_id_str]['cantidad'] -= 1
                else:
                    del carrito[producto_id_str]
                    messages.info(request, 'Producto eliminado del carrito')

        request.session['carrito'] = carrito
        request.session.modified = True

    return redirect('tienda:ver_carrito')


def eliminar_del_carrito(request, producto_id):
    """Eliminar producto del carrito"""
    carrito = request.session.get('carrito', {})
    producto_id_str = str(producto_id)

    if producto_id_str in carrito:
        del carrito[producto_id_str]
        messages.success(request, 'Producto eliminado del carrito')

    request.session['carrito'] = carrito
    request.session.modified = True

    return redirect('tienda:ver_carrito')


def checkout(request):
    """Proceso de pago seguro"""
    carrito = request.session.get('carrito', {})

    if not carrito:
        messages.warning(request, 'Tu carrito está vacío')
        return redirect('index')

    items = []
    total = 0

    # Recalcular todo desde DB (y validar stock)
    for producto_id, item in carrito.items():
        producto = get_object_or_404(Producto, id=int(producto_id), activo=True)
        cantidad = int(item['cantidad'])

        if cantidad <= 0:
            messages.warning(request, 'Hay un producto con cantidad inválida en el carrito.')
            return redirect('ver_carrito')

        if cantidad > producto.stock:
            messages.warning(
                request,
                f'No hay stock suficiente de {producto.nombre}. Disponible: {producto.stock}'
            )
            return redirect('ver_carrito')

        subtotal = float(producto.precio) * cantidad
        total += subtotal

        items.append({
            'producto': producto,
            'cantidad': cantidad,
            'precio': float(producto.precio),
        })

    if request.method == 'POST':
        with transaction.atomic():

            # Crear el pedido
            pedido = Pedido.objects.create(
                nombre_cliente=request.POST.get('nombre'),
                telefono=request.POST.get('telefono'),
                direccion=request.POST.get('direccion'),
                email=request.POST.get('email', ''),
                comprobante_sinpe=request.POST.get('comprobante'),
                total=total,
            )

            # Crear items y descontar stock con verificación
            for item in items:
                ItemPedido.objects.create(
                    pedido=pedido,
                    producto=item['producto'],
                    cantidad=item['cantidad'],
                    precio_unitario=item['precio'],
                )

                updated = Producto.objects.filter(
                    id=item['producto'].id,
                    stock__gte=item['cantidad']
                ).update(stock=F('stock') - item['cantidad'])

                # Si no actualizó, significa que el stock cambió entre validación y pago
                if updated == 0:
                    messages.warning(
                        request,
                        f'El stock de {item["producto"].nombre} cambió. Intenta de nuevo.'
                    )
                    # Lanzamos excepción para que se revierta la transacción
                    raise ValueError("Stock cambió durante el checkout")

            # Limpiar carrito
            request.session['carrito'] = {}
            request.session.modified = True

            return redirect('tienda:confirmacion_pedido', pedido_id=pedido.id)

    return render(request, 'tienda/checkout.html', {
        'items': items,
        'total': total,
    })


def confirmacion_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'tienda/confirmacion.html', {'pedido': pedido})


def vaciar_carrito(request):
    request.session['carrito'] = {}
    request.session.modified = True
    messages.success(request, 'Carrito vaciado')
    return redirect('index')
