from django.contrib import admin
from .models import Categoria, Producto, Pedido, ItemPedido


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "emoji", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre", "descripcion")
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio", "stock", "activo", "actualizado")
    list_filter = ("activo", "categoria")
    search_fields = ("nombre", "descripcion")
    prepopulated_fields = {"slug": ("nombre",)}
    ordering = ("-creado",)


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    autocomplete_fields = ("producto",)
    readonly_fields = ()  # puedes poner ("subtotal",) si lo vuelves field en admin


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre_cliente", "telefono", "total", "estado", "creado")
    list_filter = ("estado", "creado")
    search_fields = ("nombre_cliente", "telefono", "email", "comprobante_sinpe")
    date_hierarchy = "creado"
    inlines = [ItemPedidoInline]


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ("pedido", "producto", "cantidad", "precio_unitario")
    search_fields = ("pedido__nombre_cliente", "producto__nombre")
    list_filter = ("pedido__estado",)
