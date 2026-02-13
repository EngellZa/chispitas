from django.core.management.base import BaseCommand
from tienda.models import Categoria, Producto


class Command(BaseCommand):
    help = 'Pobla la base de datos con productos de ejemplo'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creando categorías...')
        
        # Crear categorías
        categorias_data = [
            {'nombre': 'Ropa', 'emoji': '👗', 'descripcion': 'Vestidos, conjuntos y más'},
            {'nombre': 'Juguetes', 'emoji': '🧸', 'descripcion': 'Muñecas, juegos y diversión'},
            {'nombre': 'Accesorios', 'emoji': '🎀', 'descripcion': 'Moños, joyas y complementos'},
            {'nombre': 'Escolares', 'emoji': '📚', 'descripcion': 'Útiles y material escolar'},
        ]
        
        categorias = {}
        for cat_data in categorias_data:
            cat, created = Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={
                    'emoji': cat_data['emoji'],
                    'descripcion': cat_data['descripcion']
                }
            )
            categorias[cat.nombre] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Categoría creada: {cat.nombre}'))
        
        self.stdout.write('\nCreando productos...')
        
        # Crear productos
        productos_data = [
            # Ropa
            {'nombre': 'Vestido Princesa Rosa', 'categoria': 'Ropa', 'precio': 15000, 'imagen': '👗', 'descripcion': 'Hermoso vestido con tul y brillos', 'stock': 5},
            {'nombre': 'Conjunto Unicornio', 'categoria': 'Ropa', 'precio': 12000, 'imagen': '👕', 'descripcion': 'Set de blusa y pantalón', 'stock': 8},
            {'nombre': 'Tutú Bailarina', 'categoria': 'Ropa', 'precio': 8500, 'imagen': '🩰', 'descripcion': 'Tutú esponjoso multicolor', 'stock': 10},
            {'nombre': 'Pijama de Estrellas', 'categoria': 'Ropa', 'precio': 9500, 'imagen': '🌟', 'descripcion': 'Pijama suave y cómoda', 'stock': 12},
            
            # Juguetes
            {'nombre': 'Muñeca Fashion', 'categoria': 'Juguetes', 'precio': 18000, 'imagen': '👸', 'descripcion': 'Muñeca con accesorios', 'stock': 6},
            {'nombre': 'Set de Cocina', 'categoria': 'Juguetes', 'precio': 22000, 'imagen': '🍳', 'descripcion': 'Cocinita con utensilios', 'stock': 4},
            {'nombre': 'Peluche Unicornio', 'categoria': 'Juguetes', 'precio': 13500, 'imagen': '🦄', 'descripcion': 'Suave y abrazable', 'stock': 12},
            {'nombre': 'Casa de Muñecas', 'categoria': 'Juguetes', 'precio': 35000, 'imagen': '🏠', 'descripcion': 'Casa de 3 pisos con muebles', 'stock': 3},
            
            # Accesorios
            {'nombre': 'Diadema con Moño', 'categoria': 'Accesorios', 'precio': 3500, 'imagen': '🎀', 'descripcion': 'Varios colores disponibles', 'stock': 20},
            {'nombre': 'Mochila Estrellitas', 'categoria': 'Accesorios', 'precio': 16000, 'imagen': '🎒', 'descripcion': 'Espaciosa y resistente', 'stock': 7},
            {'nombre': 'Joyería de Fantasía', 'categoria': 'Accesorios', 'precio': 5000, 'imagen': '💍', 'descripcion': 'Set de collar y pulseras', 'stock': 15},
            {'nombre': 'Gafas de Sol', 'categoria': 'Accesorios', 'precio': 4500, 'imagen': '🕶️', 'descripcion': 'Gafas con protección UV', 'stock': 10},
            
            # Escolares
            {'nombre': 'Cuadernos Decorados', 'categoria': 'Escolares', 'precio': 4000, 'imagen': '📓', 'descripcion': 'Pack de 3 cuadernos', 'stock': 25},
            {'nombre': 'Set de Colores Premium', 'categoria': 'Escolares', 'precio': 9500, 'imagen': '🖍️', 'descripcion': '48 colores brillantes', 'stock': 10},
            {'nombre': 'Lonchera Térmica', 'categoria': 'Escolares', 'precio': 12500, 'imagen': '🍱', 'descripcion': 'Mantiene fresco por horas', 'stock': 8},
            {'nombre': 'Estuche Multiusos', 'categoria': 'Escolares', 'precio': 6500, 'imagen': '✏️', 'descripcion': 'Con compartimentos', 'stock': 15},
        ]
        
        for prod_data in productos_data:
            categoria = categorias[prod_data['categoria']]
            producto, created = Producto.objects.get_or_create(
                nombre=prod_data['nombre'],
                defaults={
                    'categoria': categoria,
                    'precio': prod_data['precio'],
                    'imagen': prod_data['imagen'],
                    'descripcion': prod_data['descripcion'],
                    'stock': prod_data['stock'],
                    'activo': True,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Producto creado: {producto.nombre}'))
        
        self.stdout.write(self.style.SUCCESS('\n¡Base de datos poblada exitosamente! ✨'))
