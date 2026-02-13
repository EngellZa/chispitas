@echo off
echo ==================================
echo    Chispitas - Inicio Rapido    
echo ==================================
echo.

echo 1. Creando entorno virtual...
python -m venv venv

echo 2. Activando entorno virtual...
call venv\Scripts\activate

echo 3. Instalando dependencias...
pip install -r requirements.txt

echo 4. Creando base de datos...
python manage.py makemigrations
python manage.py migrate

echo 5. Creando superusuario...
echo Por favor ingresa los datos para el administrador:
python manage.py createsuperuser

echo 6. Poblando base de datos con productos de ejemplo...
python manage.py poblar_db

echo.
echo ==================================
echo    Instalacion Completada!
echo ==================================
echo.
echo Para iniciar el servidor ejecuta:
echo   python manage.py runserver
echo.
echo Luego abre en tu navegador:
echo   http://localhost:8000
echo.
echo Panel de administracion:
echo   http://localhost:8000/admin
echo.
pause
