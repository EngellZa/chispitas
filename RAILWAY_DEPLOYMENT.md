# 🚀 Guía de Despliegue en Railway

Esta guía te ayudará a desplegar tu tienda Chispitas en Railway con base de datos PostgreSQL y Cloudinary para archivos.

## 📋 Pre-requisitos

1. Cuenta en [Railway](https://railway.app/)
2. Cuenta en [Cloudinary](https://cloudinary.com/) (gratis)
3. Cuenta de Gmail para enviar emails (opcional)

---

## 🔧 Paso 1: Configurar Cloudinary

1. Ve a https://cloudinary.com/ y crea una cuenta gratuita
2. En el Dashboard, encontrarás:
   - **Cloud Name**
   - **API Key**
   - **API Secret**
3. Guarda estos valores, los necesitarás después

---

## 📧 Paso 2: Configurar Gmail (Opcional)

Para enviar emails de confirmación:

1. Ve a tu cuenta de Google
2. Activa la verificación en 2 pasos
3. Genera una "Contraseña de aplicación":
   - Ve a: https://myaccount.google.com/apppasswords
   - Selecciona "Correo" y "Otro"
   - Nombra: "Chispitas Django"
   - Copia la contraseña de 16 caracteres

---

## 🚂 Paso 3: Desplegar en Railway

### A. Crear Proyecto desde GitHub

1. **Sube tu código a GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Chispitas E-commerce"
   git remote add origin https://github.com/TU-USUARIO/chispitas.git
   git push -u origin main
   ```

2. **En Railway**:
   - Ve a https://railway.app/
   - Click en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Conecta tu repositorio
   - Railway detectará automáticamente que es Django

### B. Agregar PostgreSQL

1. En tu proyecto de Railway:
   - Click en "+ New"
   - Selecciona "Database" → "PostgreSQL"
   - Railway creará automáticamente la variable `DATABASE_URL`

### C. Configurar Variables de Entorno

En Railway, ve a tu servicio → "Variables" y agrega:

```bash
# Django
SECRET_KEY=genera-una-clave-secreta-super-segura-aqui-usa-random-org
DEBUG=False
ALLOWED_HOSTS=*.railway.app

# Cloudinary (usa tus valores del Paso 1)
CLOUDINARY_CLOUD_NAME=tu-cloud-name-aqui
CLOUDINARY_API_KEY=tu-api-key-aqui
CLOUDINARY_API_SECRET=tu-api-secret-aqui

# Email (opcional, usa tus valores del Paso 2)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-contraseña-de-aplicacion-de-16-caracteres
DEFAULT_FROM_EMAIL=Chispitas <noreply@chispitas.cr>
```

**Generar SECRET_KEY seguro:**
```python
# En tu terminal local con Python:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 🎯 Paso 4: Deploy y Verificación

1. **Railway desplegará automáticamente** cuando detecte los cambios
2. **Espera** a que termine el despliegue (2-5 minutos)
3. Railway te dará una URL como: `https://chispitas.railway.app`

---

## 👨‍💼 Paso 5: Crear Superusuario

Para acceder al panel admin:

1. En Railway, ve a tu servicio
2. Click en "Settings" → "Deploy Triggers"
3. O usa Railway CLI:

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link al proyecto
railway link

# Crear superusuario
railway run python manage.py createsuperuser
```

---

## 📊 Paso 6: Poblar la Base de Datos

```bash
# Usando Railway CLI
railway run python manage.py poblar_db
```

O hazlo desde el admin de Django después de crear el superusuario.

---

## ✅ Verificación Final

1. **Tienda**: https://tu-app.railway.app/
2. **Admin**: https://tu-app.railway.app/admin/
3. **Prueba**:
   - Agrega productos al carrito
   - Completa el checkout
   - Sube un comprobante SINPE
   - Verifica que el archivo se guardó en Cloudinary
   - Verifica que llegó el email (si configuraste)

---

## 🔄 Actualizar tu Aplicación

Cada vez que hagas cambios:

```bash
git add .
git commit -m "Descripción de cambios"
git push
```

Railway desplegará automáticamente los cambios.

---

## 🛠️ Comandos Útiles de Railway CLI

```bash
# Ver logs en tiempo real
railway logs

# Ejecutar comandos
railway run python manage.py migrate
railway run python manage.py collectstatic

# Abrir shell de Python
railway run python manage.py shell

# Ver variables de entorno
railway variables
```

---

## 📱 Configurar Dominio Personalizado (Opcional)

1. En Railway → Settings → Domains
2. Click en "Generate Domain" o "Custom Domain"
3. Sigue las instrucciones para configurar DNS

---

## 🐛 Solución de Problemas

### Error: "DisallowedHost"
- Verifica que `ALLOWED_HOSTS` incluya `*.railway.app`

### Error: "No module named 'cloudinary'"
- Verifica que `requirements.txt` esté correcto
- Railway debería instalar automáticamente

### Error al subir archivos
- Verifica las credenciales de Cloudinary
- Verifica que las variables de entorno estén bien escritas

### Emails no se envían
- Verifica la contraseña de aplicación de Gmail
- Verifica que `EMAIL_HOST_USER` sea correcto
- Revisa los logs: `railway logs`

### Base de datos vacía
- Ejecuta: `railway run python manage.py poblar_db`
- O crea productos manualmente desde el admin

---

## 💰 Costos

- **Railway**: Plan gratuito incluye $5 de crédito mensual
- **Cloudinary**: 25GB de almacenamiento gratuito
- **Gmail**: Gratis para envío de emails

---

## 📚 Recursos Adicionales

- [Documentación de Railway](https://docs.railway.app/)
- [Documentación de Cloudinary](https://cloudinary.com/documentation)
- [Documentación de Django](https://docs.djangoproject.com/)

---

## 🎉 ¡Listo!

Tu tienda Chispitas está ahora en producción. ¡Felicidades! 🎊

Para soporte adicional, revisa los logs:
```bash
railway logs --follow
```
