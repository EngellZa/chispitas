from django.db import models
from django.utils.text import slugify


class Categoria(models.Model):
    """Modelo para las categorías de productos"""
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    emoji = models.CharField(max_length=10, default='✨')
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """Modelo para los productos"""
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.CharField(max_length=10, default='🎁', help_text='Emoji del producto')
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-destacado', '-fecha_creacion']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre
    
    @property
    def precio_formateado(self):
        return f"₡{self.precio:,.0f}".replace(',', '.')
    
    def esta_disponible(self):
        return self.activo and self.stock > 0


class Pedido(models.Model):
    """Modelo para los pedidos"""
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    nombre_cliente = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    email = models.EmailField(blank=True)
    comprobante_sinpe = models.CharField(max_length=50, help_text='Número de comprobante SINPE')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    notas = models.TextField(blank=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha_pedido']
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.nombre_cliente}"
    
    @property
    def total_formateado(self):
        return f"₡{self.total:,.0f}".replace(',', '.')


class ItemPedido(models.Model):
    """Modelo para los items de cada pedido"""
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Item de Pedido'
        verbose_name_plural = 'Items de Pedido'
    
    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre}"
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
    
    @property
    def subtotal_formateado(self):
        return f"₡{self.subtotal:,.0f}".replace(',', '.')
