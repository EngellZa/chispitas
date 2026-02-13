from django.contrib import admin
from apps.tienda.models import Categoria, Producto, Pedido, ItemPedido


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'emoji', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'stock', 'activo', 'destacado']
    list_filter = ['categoria', 'activo', 'destacado']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock', 'activo', 'destacado']
    prepopulated_fields = {'slug': ('nombre',)}


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ['producto', 'cantidad', 'precio_unitario', 'subtotal_formateado']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre_cliente', 'telefono', 'total_formateado', 'estado', 'fecha_pedido']
    list_filter = ['estado', 'fecha_pedido']
    search_fields = ['nombre_cliente', 'telefono', 'comprobante_sinpe']
    list_editable = ['estado']
    readonly_fields = ['fecha_pedido', 'fecha_actualizacion']
    inlines = [ItemPedidoInline]
    
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('nombre_cliente', 'telefono', 'email', 'direccion')
        }),
        ('Información del Pedido', {
            'fields': ('comprobante_sinpe', 'total', 'estado', 'notas')
        }),
        ('Fechas', {
            'fields': ('fecha_pedido', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
