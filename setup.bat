@echo off

REM Doña Pepa Backend Setup Script for Windows

echo 🍵 Doña Pepa FastAPI Backend Setup
echo ==================================

REM Check Python version
python --version
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.10+
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
) else (
    echo ✓ Virtual environment exists
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt --quiet

REM Check if .env exists
if not exist ".env" (
    echo ⚙️  Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Edit .env with your database credentials
) else (
    echo ✓ .env file exists
)

REM Initialize database
echo 🗄️  Initializing database...
python db_init.py seed

echo.
echo ✅ Setup complete!
echo.
echo To start the development server:
echo   venv\Scripts\activate
echo   python main.py
echo.
echo API will be available at: http://localhost:8000
echo Documentation at: http://localhost:8000/docs
pause
