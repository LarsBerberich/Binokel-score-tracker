# Pull Request Review Checkliste

Eine schnelle Checkliste für typische Review-Szenarien im Binokel Score Tracker Projekt.

## 🔍 Allgemeine Code Review Checkliste

### Code Quality
- [ ] Code ist lesbar und gut strukturiert
- [ ] Variablen und Funktionen haben aussagekräftige Namen
- [ ] Keine duplizierten Code-Blöcke
- [ ] Kommentare vorhanden wo nötig (komplexe Logik)
- [ ] Code folgt Python/Django Konventionen (PEP 8)

### Funktionalität
- [ ] Code macht was er soll (funktionale Anforderungen erfüllt)
- [ ] Edge Cases sind behandelt
- [ ] Error Handling ist angemessen
- [ ] Performance ist akzeptabel

### Tests
- [ ] Alle bestehenden Tests laufen durch: `python manage.py test`
- [ ] Neue Features haben entsprechende Tests
- [ ] Test Coverage ist angemessen
- [ ] Tests sind aussagekräftig und nicht trivial

## 🎯 Django-spezifische Checkliste

### Models (`score_tracker/models.py`)
- [ ] Field-Typen sind korrekt gewählt
- [ ] Relationships (ForeignKey, ManyToMany) sind richtig definiert
- [ ] `__str__` Methoden sind implementiert
- [ ] Meta-Optionen sind sinnvoll (unique_together, ordering, etc.)
- [ ] Validierung auf Model-Level wenn nötig

### Views (`score_tracker/views.py`)
- [ ] Correct HTTP methods (GET, POST) verwendet
- [ ] Authentication/Authorization wenn nötig
- [ ] Proper error handling (404, 403, etc.)
- [ ] Context-Data ist vollständig
- [ ] Redirects sind korrekt implementiert

### Forms (`score_tracker/forms.py`)
- [ ] Form-Validierung ist vollständig
- [ ] Clean-Methods sind korrekt implementiert
- [ ] Widgets sind angemessen gewählt
- [ ] Help-Texte und Labels sind benutzerfreundlich

### Templates (`templates/`)
- [ ] HTML ist valide
- [ ] XSS-Schutz durch `|escape` oder `{% autoescape %}`
- [ ] Template-Tags sind korrekt verwendet
- [ ] Responsive Design (falls relevant)
- [ ] Accessibility berücksichtigt

### URLs (`score_tracker/urls.py`)
- [ ] URL-Pattern sind korrekt
- [ ] Namen sind eindeutig und beschreibend
- [ ] Parameter werden korrekt übergeben

### Migrations
- [ ] Migrations sind rückwärts-kompatibel (wenn möglich)
- [ ] `makemigrations --dry-run` zeigt erwartete Änderungen
- [ ] Keine sensible Daten in Migrations

## 🎮 Binokel-spezifische Business Logic

### Scoring System
- [ ] Punkte-Berechnung ist korrekt
  - Meldungen: richtige Punktwerte
  - Stiche: max 250 Punkte
  - Bid-Erfüllung: Logik ist korrekt
- [ ] "Abgehen" wird richtig behandelt
- [ ] "Durch" wird richtig behandelt
- [ ] Rundengewinn bei 1000+ Punkten

### Game Flow
- [ ] Spiel-Status (aktiv/beendet) wird korrekt verwaltet
- [ ] Runden-Reihenfolge ist richtig
- [ ] Player-Zuordnung funktioniert
- [ ] End-Game Logic ist korrekt

## 🧪 Testing Checkliste

### Vor dem Review
```bash
# Virtual Environment aktivieren
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate     # Windows

# Dependencies installieren
pip install -r requirements.txt

# Django Check
python manage.py check

# Migrations
python manage.py migrate

# Tests ausführen
python manage.py test --verbosity=2
```

### Test-Kategorien prüfen
- [ ] **Unit Tests**: Individual Komponenten (Models, Forms)
- [ ] **Integration Tests**: Zusammenspiel verschiedener Komponenten
- [ ] **View Tests**: HTTP Requests/Responses
- [ ] **Form Tests**: Validierung und Datenverarbeitung

### Spezifische Test-Commands
```bash
# Nur Model Tests
python manage.py test score_tracker.tests.GameModelTest

# Mit Coverage (falls installiert)
coverage run manage.py test
coverage report

# Behave Tests (falls vorhanden)
python manage.py behave
```

## 🚀 Performance Checkliste

### Database
- [ ] Keine N+1 Query-Probleme
- [ ] `select_related()` und `prefetch_related()` wo sinnvoll
- [ ] Database Indexes auf häufig abgefragte Felder
- [ ] Queries sind effizient (Django Debug Toolbar nutzen)

### Frontend
- [ ] Static Files werden korrekt geladen
- [ ] CSS/JS ist minimiert (in Production)
- [ ] Images sind optimiert
- [ ] Keine unnötigen HTTP Requests

## 🔒 Security Checkliste

### Django Security
- [ ] CSRF Protection aktiviert
- [ ] XSS-Schutz in Templates
- [ ] SQL Injection durch ORM verhindert
- [ ] Proper Authentication/Authorization
- [ ] Sensitive Daten nicht in Git

### Input Validation
- [ ] Alle User Inputs werden validiert
- [ ] File Uploads sind sicher (falls relevant)
- [ ] Rate Limiting bei nötigen Endpoints

## 📱 UI/UX Checkliste (falls UI-Änderungen)

### Usability
- [ ] Interface ist intuitiv
- [ ] Error Messages sind benutzerfreundlich
- [ ] Success/Feedback Messages werden angezeigt
- [ ] Navigation ist logisch

### Design
- [ ] Bootstrap-Klassen werden konsistent verwendet
- [ ] Layout ist responsive
- [ ] Farben und Schriftarten sind konsistent
- [ ] Accessibility-Standards beachtet

### Browser Testing
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari (falls Mac vorhanden)
- [ ] Mobile Browsers (falls relevant)

## ✅ Quick Review Commands

```bash
# Setup und Tests
./setup_dev.sh              # Komplette Entwicklungsumgebung
python manage.py test        # Alle Tests
python manage.py check       # Django System Check
python manage.py runserver   # Development Server

# Code Quality
python -m flake8 .           # Code Linting
python manage.py check --deploy  # Production Readiness

# Git Commands
git diff main...HEAD         # Alle Änderungen anzeigen
git log main..HEAD --oneline # Commit History
git diff --name-only main...HEAD  # Geänderte Dateien
```

## 📋 Review Kommentar-Templates

### Code Improvements
```
💡 **Suggestion**: Consider using `select_related()` here to avoid N+1 queries.
```

### Security Issues
```
🔒 **Security**: This user input should be validated/escaped to prevent XSS.
```

### Performance
```
⚡ **Performance**: This loop could be optimized by moving the query outside.
```

### Style Issues
```
🎨 **Style**: Consider following PEP 8 naming conventions (snake_case for functions).
```

### Questions
```
❓ **Question**: What happens if `game.is_active` is False here?
```

### Approval
```
✅ **LGTM**: Great implementation! Tests pass and code is clean.
```