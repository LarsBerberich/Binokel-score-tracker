# Contributing to Binokel Score Tracker

Vielen Dank für Ihr Interesse, zum Binokel Score Tracker beizutragen! / Thank you for your interest in contributing to the Binokel Score Tracker!

## Wo finde ich Pull Requests zum Review? / Where can I find Pull Requests to review?

### Deutsch
Pull Requests zum Review finden Sie hier:

1. **Alle Pull Requests ansehen**: [https://github.com/LarsBerberich/Binokel-score-tracker/pulls](https://github.com/LarsBerberich/Binokel-score-tracker/pulls)
2. **Offene Pull Requests**: [https://github.com/LarsBerberich/Binokel-score-tracker/pulls?q=is%3Aopen](https://github.com/LarsBerberich/Binokel-score-tracker/pulls?q=is%3Aopen)
3. **Draft Pull Requests**: [https://github.com/LarsBerberich/Binokel-score-tracker/pulls?q=is%3Adraft](https://github.com/LarsBerberich/Binokel-score-tracker/pulls?q=is%3Adraft)

### English
You can find Pull Requests to review here:

1. **View all Pull Requests**: [https://github.com/LarsBerberich/Binokel-score-tracker/pulls](https://github.com/LarsBerberich/Binokel-score-tracker/pulls)
2. **Open Pull Requests**: [https://github.com/LarsBerberich/Binokel-score-tracker/pulls?q=is%3Aopen](https://github.com/LarsBerberich/Binokel-score-tracker/pulls?q=is%3Aopen)
3. **Draft Pull Requests**: [https://github.com/LarsBerberich/Binokel-score-tracker/pulls?q=is%3Adraft](https://github.com/LarsBerberich/Binokel-score-tracker/pulls?q=is%3Adraft)

## Wie reviewe ich einen Pull Request? / How to review a Pull Request?

### Deutsch
1. Klicken Sie auf einen Pull Request aus der Liste
2. Gehen Sie zum Tab **"Files changed"** um die Code-Änderungen zu sehen
3. Fügen Sie Kommentare zu bestimmten Zeilen hinzu, indem Sie auf das "+" Symbol klicken
4. Nutzen Sie den **"Review changes"** Button um:
   - **Comment**: Allgemeines Feedback geben
   - **Approve**: Die Änderungen genehmigen
   - **Request changes**: Änderungen vor dem Merge anfordern

### English
1. Click on any Pull Request from the list
2. Go to the **"Files changed"** tab to see the code changes
3. Add comments to specific lines by clicking the "+" icon
4. Use the **"Review changes"** button to:
   - **Comment**: Provide general feedback
   - **Approve**: Approve the changes
   - **Request changes**: Request modifications before merging

## Development Setup

### Prerequisites
- Python 3.8+
- Django 4.2.8
- Git

### Setup Instructions
```bash
# Clone the repository
git clone https://github.com/LarsBerberich/Binokel-score-tracker.git
cd Binokel-score-tracker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

## How to Contribute

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** and test them locally
4. **Commit your changes**: `git commit -m "Description of changes"`
5. **Push to your fork**: `git push origin feature/your-feature-name`
6. **Create a Pull Request** from your fork to this repository

## Guidelines

### Code Style
- Follow Django best practices
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small

### Testing
- Write tests for new features
- Run existing tests to ensure nothing breaks
- Use Django's testing framework
- For BDD tests, use behave-django

```bash
# Run Django tests
python manage.py test

# Run BDD tests
python manage.py behave
```

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, etc.)
- Keep the first line under 50 characters
- Add more details in the body if needed

Example:
```
Add game statistics to dashboard

- Display total games played
- Show average scores per player
- Add winning percentage calculations
```

## Project Structure

- `binokel_project/` - Django project settings
- `score_tracker/` - Main application code
- `templates/` - HTML templates
- `static/` - CSS, JavaScript, and images
- `requirements.txt` - Python dependencies

## Questions?

If you have questions:
1. Check existing [Issues](https://github.com/LarsBerberich/Binokel-score-tracker/issues)
2. Create a new issue for bugs or feature requests
3. Use Pull Request comments for code-specific discussions