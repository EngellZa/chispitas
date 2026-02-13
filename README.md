# 🌟 Chispitas - E-commerce para Productos de Niñas en Costa Rica

E-commerce completo desarrollado en Django con integración de pago SINPE Móvil para Costa Rica.

## ✨ Características

- 🛍️ **Catálogo de Productos**: Sistema completo de productos con categorías
- 🛒 **Carrito de Compras**: Gestión de carrito con sesiones
- 💳 **Pago SINPE**: Integración para pagos con SINPE Móvil
- 📱 **Responsive**: Diseño adaptable a móviles y desktop
- 🎨 **Diseño Atractivo**: Interfaz colorida y alegre para niñas
- 📊 **Panel de Admin**: Gestión completa desde Django Admin
- 🔒 **Sistema de Pedidos**: Gestión y seguimiento de pedidos

## 🚀 Instalación

### 1. Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 2. Instalación Paso a Paso

```bash
# 1. Crear y activar entorno virtual (recomendado)
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Mac/Linux:
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Crear las migraciones de la base de datos
python manage.py makemigrations
python manage.py migrate

# 4. Crear un superusuario para acceder al admin
python manage.py createsuperuser
# Sigue las instrucciones en pantalla

# 5. Poblar la base de datos con productos de ejemplo
python manage.py poblar_db

# 6. Ejecutar el servidor de desarrollo
python manage.py runserver
```

### 3. Acceder a la Aplicación

- **Tienda**: http://localhost:8000/
- **Panel de Admin**: http://localhost:8000/admin/

## 📁 Estructura del Proyecto

```
chispitas_django/
├── chispitas_project/          # Configuración del proyecto
│   ├── settings.py            # Configuraciones
│   ├── urls.py                # URLs principales
│   └── wsgi.py                # WSGI config
├── tienda/                     # App principal
│   ├── models.py              # Modelos (Producto, Pedido, etc.)
│   ├── views.py               # Vistas
│   ├── urls.py                # URLs de la tienda
│   ├── admin.py               # Configuración del admin
│   ├── templates/             # Plantillas HTML
│   │   └── tienda/
│   │       ├── base.html      # Plantilla base
│   │       ├── index.html     # Página principal
│   │       ├── carrito.html   # Carrito de compras
│   │       ├── checkout.html  # Proceso de pago
│   │       └── confirmacion.html
│   └── management/
│       └── commands/
│           └── poblar_db.py   # Comando para datos de prueba
├── manage.py                   # Utilidad de Django
└── requirements.txt            # Dependencias del proyecto
```

## 🎯 Funcionalidades Principales

### 1. Gestión de Productos
- Crear, editar y eliminar productos
- Organizar por categorías
- Control de stock
- Productos destacados

### 2. Sistema de Carrito
- Agregar/eliminar productos
- Ajustar cantidades
- Validación de stock
- Persistencia en sesión

### 3. Proceso de Pago SINPE
- Instrucciones claras para el usuario
- Formulario de datos del cliente
- Registro de comprobante SINPE
- Confirmación de pedido

### 4. Panel de Administración
Accede a http://localhost:8000/admin/ para:
- Gestionar productos y categorías
- Ver y actualizar pedidos
- Cambiar estados de pedidos
- Ver detalles de compras

## 🛠️ Personalización

### Cambiar el Número SINPE
Edita `tienda/templates/tienda/checkout.html` y busca:
```html
<p class="text-3xl font-bold text-blue-600 tracking-wider">8888-8888</p>
```
Reemplaza con tu número real.

### Agregar Productos
Dos opciones:
1. **Desde el Admin**: http://localhost:8000/admin/tienda/producto/
2. **Por código**: Edita `tienda/management/commands/poblar_db.py`

### Modificar Categorías
Edita en `tienda/management/commands/poblar_db.py` o desde el admin.

### Personalizar Diseño
- **Colores**: Edita `tienda/templates/tienda/base.html` (CSS en `<style>`)
- **Templates**: Modifica archivos en `tienda/templates/tienda/`

## 📧 Configuración de Email (Opcional)

Para enviar emails de confirmación, agrega en `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # o tu proveedor
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu-contraseña-de-app'
```

## 🚀 Despliegue en Producción

### Preparación
1. Cambiar `DEBUG = False` en `settings.py`
2. Configurar `ALLOWED_HOSTS` con tu dominio
3. Configurar base de datos PostgreSQL o MySQL
4. Recolectar archivos estáticos:
```bash
python manage.py collectstatic
```

### Opciones de Hosting
- **Heroku**: Fácil y gratuito para empezar
- **PythonAnywhere**: Hosting Python específico
- **DigitalOcean**: VPS con más control
- **AWS/Google Cloud**: Escalable para producción

## 📝 Modelos de Datos

### Producto
- Nombre, descripción, precio
- Categoría
- Stock disponible
- Imagen (emoji)
- Estado (activo/inactivo)

### Pedido
- Información del cliente
- Comprobante SINPE
- Total
- Estado (pendiente, confirmado, enviado, etc.)
- Items del pedido

### Categoría
- Nombre
- Emoji representativo
- Descripción

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Puedes:
- Reportar bugs
- Sugerir nuevas características
- Mejorar la documentación
- Enviar pull requests

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso personal y comercial.

## 💡 Próximos Pasos Sugeridos

1. **Integración WhatsApp API**: Notificaciones automáticas
2. **Galería de Imágenes**: Subir imágenes reales de productos
3. **Sistema de Usuarios**: Registro y login de clientes
4. **Historial de Pedidos**: Clientes pueden ver sus compras
5. **Cupones de Descuento**: Sistema de promociones
6. **Envío por Zonas**: Calcular costos de envío
7. **Reviews de Productos**: Opiniones de clientes
8. **Dashboard de Ventas**: Estadísticas y reportes

## 📞 Contacto

Para soporte o consultas sobre el proyecto, puedes:
- Abrir un issue en el repositorio
- Contactar al desarrollador

---

✨ **¡Hecho con amor para Chispitas!** 💖
