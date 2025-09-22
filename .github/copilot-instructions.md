# Copilot Instructions for Binokel Score Tracker

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Repository Overview

This is a Django web application for tracking scores in Binokel, a traditional 3-player Swabian card game. The application manages players, games, rounds, and complex scoring calculations including bid amounts, meld points, trick points, and special game variants like "abgehen" (going down) and "Durch" (taking all tricks).

**Key Technologies:**
- Django 4.2.8 (Python web framework)
- Python 3.11+ (tested with 3.12)
- PostgreSQL (production database)
- SQLite (development database)
- Bootstrap 5 (frontend framework)
- WhiteNoise (static file serving)
- Gunicorn (WSGI server)
- Docker & Docker Compose

**Repository Size:** Small Django project (~15 core Python files, ~500 lines of application code)

## Build and Development Instructions

### Environment Setup
**Always install dependencies first:**
```bash
pip install -r requirements.txt
```
Time: ~15 seconds. NEVER CANCEL: Set timeout to 60+ seconds for pip install commands.

### Essential Development Commands (in order)

1. **Database Setup (required for any work):**
```bash
python manage.py migrate
```
Time: ~1 second. Creates SQLite database with all required tables.

2. **Static Files (required before running server):**
```bash
python manage.py collectstatic --noinput
```
Time: ~1 second. Collects static files to `staticfiles/` directory.

3. **Run Tests (validate before changes):**
```bash
python manage.py test
```
Time: ~1 second. Runs 44 tests (unit, integration, and view tests). All tests must pass.

4. **Development Server:**
```bash
python manage.py runserver 8000
```
Access at http://127.0.0.1:8000/. Server auto-reloads on file changes.

5. **Configuration Check:**
```bash
python manage.py check
```
Time: ~1 second. Validates Django configuration. Must show "0 issues" before deploying.

### Docker Development (Alternative)
```bash
docker compose up --build
```
**IMPORTANT:** Docker build may fail in sandboxed environments due to SSL certificate issues. Use native Python development instead in such environments.
Time: ~30 seconds first build, ~5 seconds subsequent runs. Includes PostgreSQL database.

### Automated Setup Scripts
- Linux/Mac: `bash setup_dev.sh` - Creates virtual environment and sets up project
- Windows: `setup_dev.bat` - Windows equivalent setup script
**Note:** These scripts may fail in sandboxed environments due to network restrictions. Use manual commands above instead.

### Common Issues and Solutions

**Issue:** `django.core.exceptions.ImproperlyConfigured: SQLite 3.8.3 or later is required`
**Solution:** Ensure Python 3.11+ is being used.

**Issue:** Tests fail with database errors
**Solution:** Run `python manage.py migrate` before testing.

**Issue:** Static files not loading in development
**Solution:** Run `python manage.py collectstatic --noinput` and ensure `DEBUG=True` in settings.

**Issue:** Module import errors
**Solution:** Ensure you're in the repository root directory with `manage.py`.

## Project Architecture and Layout

### Core Application Structure
```
binokel_project/          # Django project configuration
├── settings.py           # Main settings (database, middleware, apps)
├── urls.py              # Root URL configuration
└── wsgi.py              # WSGI entry point

score_tracker/           # Main Django application
├── models.py            # Data models: Player, Game, Round, Score
├── views.py             # View functions for web pages
├── forms.py             # Django forms for user input
├── urls.py              # URL routing for the app
├── admin.py             # Django admin configuration
├── tests.py             # All tests (35 test methods)
├── migrations/          # Database migration files
└── templatetags/        # Custom template filters

templates/               # HTML templates
├── base.html            # Base template with Bootstrap
└── score_tracker/       # App-specific templates

static/                  # Source static files
├── css/                 # Custom CSS files
└── js/                  # Custom JavaScript files

staticfiles/             # Generated static files (build artifact)
```

### Key Configuration Files
- `requirements.txt` - Python dependencies (Django, PostgreSQL driver, testing tools)
- `Dockerfile` - Container configuration using Python 3.11-slim
- `docker-compose.yml` - Development environment with PostgreSQL
- `manage.py` - Django management command entry point

### Model Relationships
- **Player:** Basic player information with name and timestamps
- **Game:** Contains multiple players (ManyToMany), tracks active state and dates
- **Round:** Belongs to Game, has game_maker (Player), bid amount, success status
- **Score:** Links Round and Player, stores meld_points and trick_points

### Critical Business Logic
Located in `score_tracker/models.py`:
- `Game.get_current_score()` - Complex scoring calculation for all players
- Round scoring varies based on success/failure and game variants
- Score rounding to nearest 10 points
- Rounds won tracking for determining game winner

## Testing and Validation

### Test Structure (44 tests total)
- **Model Tests:** Player, Game, Round, Score creation and business logic
- **View Tests:** HTTP responses, form handling, URL routing
- **Integration Tests:** Complete game workflows from creation to completion
- **Specialized Tests:** DoppeltAbgehen functionality and form validation

### Running Specific Test Categories
```bash
# All tests (44 tests in ~1 second)
python manage.py test

# Specific test class
python manage.py test score_tracker.tests.PlayerModelTest

# Verbose output
python manage.py test --verbosity=2
```

### BDD Tests
**Note:** While `behave-django` is in requirements.txt, no BDD feature files exist in the repository. The `python manage.py behave` command is not functional.

### Pre-deployment Validation
Always run these commands before committing changes:
1. `python manage.py check` (must show 0 issues)
2. `python manage.py test` (all 44 tests must pass)
3. `python manage.py migrate --check` (verify migrations are up to date)

### Manual Validation Scenarios
**ALWAYS test these user scenarios after making changes:**

1. **Homepage Access:** Navigate to http://127.0.0.1:8000/ and verify the application loads with game statistics
2. **Game Creation Workflow:**
   - Click "New Game" → Fill in at least 3 player names → Click "Create Game"
   - Verify game detail page loads with player scoreboard
3. **Core Application Logic:**
   - Create test players, games, and rounds through Django shell
   - Verify scoring calculations work correctly
   - Test game maker vs. other player scoring differences

**Screenshot Verification:** The application homepage shows a clean Bootstrap-styled interface with navigation, game statistics, and game rules information.

## Dependencies and Environment

### Python Dependencies (requirements.txt)
- **Core:** Django==4.2.8, psycopg2-binary==2.9.9
- **Frontend:** django-bootstrap5==23.3
- **Static Files:** whitenoise==6.6.0
- **Testing:** behave-django==1.4.0, selenium==4.15.2
- **Production:** gunicorn==21.2.0

### Environment Variables
- `DEBUG` - Set to 1 for development, 0 for production
- `DATABASE_URL` - PostgreSQL connection string for production
- `SECRET_KEY` - Django secret (hardcoded in development settings)

### Database Configuration
- **Development:** SQLite database created automatically
- **Production:** PostgreSQL via DATABASE_URL environment variable
- **Migrations:** Located in `score_tracker/migrations/`

## File Locations Reference

### Frequently Modified Files
- `score_tracker/models.py` - Database models and business logic
- `score_tracker/views.py` - Web request handling
- `score_tracker/forms.py` - Form definitions and validation
- `templates/score_tracker/` - HTML templates
- `static/css/` and `static/js/` - Frontend assets

### Configuration Files
- `binokel_project/settings.py` - Django settings
- `binokel_project/urls.py` - Root URL configuration
- `score_tracker/urls.py` - App URL patterns
- `requirements.txt` - Python dependencies

### Generated/Build Files (Do Not Edit)
- `staticfiles/` - Collected static files
- `db.sqlite3` - Development database
- `__pycache__/` - Python bytecode cache
- `*.pyc` files

## Development Best Practices

### Before Making Changes
1. Run `python manage.py migrate` to ensure database is current
2. Run `python manage.py test` to verify current state
3. Create a superuser if needed: `python manage.py createsuperuser`

### When Adding New Features
1. Update models in `score_tracker/models.py` if needed
2. Create and run migrations: `python manage.py makemigrations && python manage.py migrate`
3. Add tests to `score_tracker/tests.py`
4. Update views and templates as needed
5. Run full test suite before committing

### Static File Handling
- Always run `python manage.py collectstatic --noinput` after modifying static files
- Source files go in `static/`, collected files in `staticfiles/`
- WhiteNoise handles static file serving in production

## Trust These Instructions

These instructions have been validated by running all commands and testing the complete development workflow. Only search for additional information if:
- A command fails with an unexpected error
- You need to understand business logic not covered here
- Requirements change (new dependencies, different deployment target)

The development workflow is straightforward: install dependencies → migrate → collect static files → test → develop → test again.

## Critical Timeouts and "NEVER CANCEL" Warnings

**NEVER CANCEL these commands - always set appropriate timeouts:**
- `pip install -r requirements.txt`: Set timeout to 300+ seconds (actual: ~15 seconds)
- `docker compose build`: Set timeout to 600+ seconds (may fail in sandboxed environments)
- All tests complete in ~1 second, Django commands complete in ~1 second

**Command Timing Summary (measured):**
- Dependencies: ~15 seconds
- Database migration: ~1 second  
- Static file collection: ~1 second
- Test suite (44 tests): ~1 second
- Django check: ~1 second