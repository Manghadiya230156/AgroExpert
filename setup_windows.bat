@echo off
setlocal
cd /d "%~dp0agroexpert_backend"
echo Checking Python...
python --version
if errorlevel 1 goto error
echo.
echo Applying database migrations...
python manage.py migrate
if errorlevel 1 goto error
echo.
echo Running Django system checks...
python manage.py check
if errorlevel 1 goto error
echo.
echo Starting AgroExpert at http://127.0.0.1:8000/
python manage.py runserver
exit /b 0
:error
echo.
echo Setup failed. Confirm the virtual environment is activated and requirements are installed.
pause
exit /b 1
