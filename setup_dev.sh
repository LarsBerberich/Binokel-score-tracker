#!/bin/bash
# Development setup script for Binokel Score Tracker

echo "🎯 Binokel Score Tracker - Development Setup"
echo "==========================================="

# Check if python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python found: $(python --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run Django checks
echo "🔍 Running Django system check..."
python manage.py check

# Create database and run migrations
echo "🗃️ Setting up database..."
python manage.py migrate

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment:"
echo "   - Linux/Mac: source venv/bin/activate"
echo "   - Windows: venv\\Scripts\\activate"
echo ""
echo "2. Start development server:"
echo "   python manage.py runserver"
echo ""
echo "3. Run tests:"
echo "   python manage.py test"
echo ""
echo "🔗 For VS Code pull request reviews, see: VS_CODE_REVIEW_GUIDE.md"