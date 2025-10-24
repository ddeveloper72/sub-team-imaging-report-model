@echo off
REM Setup script for Xt-EHR T7.2 Imaging Reports Analysis (Windows)
REM ================================================================

echo Setting up Xt-EHR T7.2 Imaging Reports Analysis environment...

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install core requirements
echo Installing core dependencies...
pip install -r requirements.txt

REM Optional: Install development dependencies
set /p choice="Install development dependencies? (y/n): "
if /i "%choice%"=="y" (
    echo Installing development dependencies...
    pip install -r requirements-dev.txt
)

echo.
echo Setup complete!
echo.
echo To start the application:
echo 1. Activate the virtual environment:
echo    .venv\Scripts\activate.bat
echo 2. Run the Flask application:
echo    cd flask_app
echo    python app.py
echo.
echo The application will be available at http://localhost:5000

pause