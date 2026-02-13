def cart_count(request):
    """Context processor para mostrar el contador del carrito en todas las páginas"""
    carrito = request.session.get('carrito', {})
    total_items = sum(item['cantidad'] for item in carrito.values())
    return {
        'cart_count': total_items
    }
