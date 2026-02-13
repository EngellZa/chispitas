#!/bin/bash

echo "=================================="
echo "   Chispitas - Inicio Rápido    "
echo "=================================="
echo ""

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}1. Creando entorno virtual...${NC}"
python3 -m venv venv

echo -e "${BLUE}2. Activando entorno virtual...${NC}"
source venv/bin/activate

echo -e "${BLUE}3. Instalando dependencias...${NC}"
pip install -r requirements.txt

echo -e "${BLUE}4. Creando base de datos...${NC}"
python manage.py makemigrations
python manage.py migrate

echo -e "${BLUE}5. Creando superusuario...${NC}"
echo "Por favor ingresa los datos para el administrador:"
python manage.py createsuperuser

echo -e "${BLUE}6. Poblando base de datos con productos de ejemplo...${NC}"
python manage.py poblar_db

echo ""
echo -e "${GREEN}=================================="
echo "   ¡Instalación Completada! ✨   "
echo "==================================${NC}"
echo ""
echo "Para iniciar el servidor ejecuta:"
echo "  python manage.py runserver"
echo ""
echo "Luego abre en tu navegador:"
echo "  http://localhost:8000"
echo ""
echo "Panel de administración:"
echo "  http://localhost:8000/admin"
echo ""
