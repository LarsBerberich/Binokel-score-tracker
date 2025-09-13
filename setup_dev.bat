@echo off
REM Development setup script for Binokel Score Tracker (Windows)

echo 🎯 Binokel Score Tracker - Development Setup
echo ===========================================

REM Check if python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Run Django checks
echo 🔍 Running Django system check...
python manage.py check

REM Create database and run migrations
echo 🗃️ Setting up database...
python manage.py migrate

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Activate virtual environment:
echo    venv\Scripts\activate
echo.
echo 2. Start development server:
echo    python manage.py runserver
echo.
echo 3. Run tests:
echo    python manage.py test
echo.
echo 🔗 For VS Code pull request reviews, see: VS_CODE_REVIEW_GUIDE.md
pause