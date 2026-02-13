from django.urls import path
from . import views

app_name= 'tienda'

urlpatterns = [
    path('', views.index, name='index'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('actualizar/<int:producto_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('vaciar-carrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmacion/<int:pedido_id>/', views.confirmacion_pedido, name='confirmacion_pedido'),
]
