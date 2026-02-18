# ---- Base ----
FROM python:3.12-slim

# Evita buffers y crea logs inmediatos
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- System deps (Pillow + builds básicos) ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libpng-dev \
    libwebp-dev \
    && rm -rf /var/lib/apt/lists/*

# ---- Workdir ----
WORKDIR /app

# ---- Install deps ----
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---- Copy project ----
COPY . /app

# ---- Static (Railway) ----
# En Railway normalmente tendrás DJANGO_SETTINGS_MODULE y SECRET_KEY por variables
# collectstatic debe correr en build/runtime (aquí lo corremos al arrancar en CMD)
EXPOSE 8000

# ---- Start ----
# Ejecuta migraciones + collectstatic (sin pedir input) y arranca gunicorn
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn chispitas.wsgi:application --bind 0.0.0.0:$PORT"]



