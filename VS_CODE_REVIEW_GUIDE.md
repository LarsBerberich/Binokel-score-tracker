# Pull Request Review mit Visual Studio Code

Diese Anleitung erklärt, wie du Pull Requests für das Binokel Score Tracker Projekt lokal in Visual Studio Code reviewen kannst.

## Voraussetzungen

### Software Installation

1. **Visual Studio Code** - [Download](https://code.visualstudio.com/)
2. **Python 3.8+** - [Download](https://www.python.org/downloads/)
3. **Git** - [Download](https://git-scm.com/downloads)

### VS Code Extensions (Automatisch vorgeschlagen)

Die folgenden Extensions werden automatisch vorgeschlagen, wenn du das Projekt öffnest:

**Essentielle Extensions:**
- `ms-python.python` - Python Support
- `github.vscode-pull-request-github` - GitHub Pull Requests
- `eamodio.gitlens` - Git Informationen
- `batisteo.vscode-django` - Django Support

**Empfohlene Extensions:**
- `ms-python.flake8` - Python Linting
- `ms-python.black-formatter` - Code Formatting
- `mhutchie.git-graph` - Git Graph Visualization
- `donjayamanne.githistory` - Git History

## Ersteinrichtung

### 1. Repository Klonen

```bash
# Repository klonen
git clone https://github.com/LarsBerberich/Binokel-score-tracker.git
cd Binokel-score-tracker

# In VS Code öffnen
code .
```

### 2. Python Virtual Environment

```bash
# Virtual Environment erstellen
python -m venv venv

# Virtual Environment aktivieren
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Dependencies installieren
pip install -r requirements.txt
```

### 3. Django Setup

```bash
# Datenbank-Migrationen ausführen
python manage.py migrate

# Django Check ausführen
python manage.py check

# Entwicklungsserver testen (optional)
python manage.py runserver
```

## Pull Request Review Workflow

### Methode 1: GitHub Pull Request Extension (Empfohlen)

1. **GitHub Extension Setup:**
   - Installiere die `GitHub Pull Requests` Extension
   - Authentifiziere dich mit GitHub: `Cmd/Ctrl + Shift + P` → "GitHub: Sign In"

2. **Pull Request öffnen:**
   - Öffne die GitHub-Seitenleiste (GitHub Icon in der Activity Bar)
   - Navigiere zu "Pull Requests"
   - Klicke auf den PR, den du reviewen möchtest
   - Wähle "Checkout"

3. **Code Review in VS Code:**
   - Der PR Branch wird automatisch ausgecheckt
   - Geänderte Dateien werden in der "Changes" Ansicht angezeigt
   - Klicke auf Dateien um Diffs zu sehen
   - Füge Kommentare hinzu durch Klick auf "+" neben den Zeilennummern

### Methode 2: Manueller Git Workflow

1. **PR Branch auschecken:**
   ```bash
   # Remote PR branches fetchen
   git fetch origin
   
   # Liste aller remote branches anzeigen
   git branch -r
   
   # Spezifischen PR branch auschecken
   git checkout -b pr-branch-name origin/pr-branch-name
   ```

2. **Änderungen analysieren:**
   ```bash
   # Unterschiede zum main branch anzeigen
   git diff main...HEAD
   
   # Geänderte Dateien auflisten
   git diff --name-only main...HEAD
   
   # Commit History anzeigen
   git log main..HEAD --oneline
   ```

### Methode 3: Pull Request per Nummer auschecken

```bash
# PR per Nummer auschecken (z.B. PR #42)
git fetch origin pull/42/head:pr-42
git checkout pr-42
```

## Review-Prozess

### 1. Code-Analyse

**VS Code Features nutzen:**
- **Go to Definition** (`F12`) - Zu Funktions-/Klassen-Definitionen springen
- **Find All References** (`Shift + F12`) - Alle Verwendungen finden
- **Peek Definition** (`Alt + F12`) - Definition inline anzeigen
- **Problems Panel** (`Cmd/Ctrl + Shift + M`) - Linting-Fehler anzeigen

**Django-spezifische Checks:**
- Models: Feldtypen, Relationships, Meta-Optionen
- Views: Security, Performance, Error Handling
- Templates: XSS-Schutz, Template Tags korrekt verwendet
- URLs: URL-Pattern, Naming

### 2. Tests ausführen

```bash
# Alle Tests ausführen
python manage.py test

# Spezifische Test-App ausführen
python manage.py test score_tracker

# Tests mit Verbose Output
python manage.py test --verbosity=2

# Behave Tests (falls vorhanden)
python manage.py behave
```

**In VS Code:**
- Nutze das Testing Panel (`Cmd/Ctrl + Shift + T`)
- Oder Debug Configuration: "Django: Run Tests"

### 3. Funktionalität testen

```bash
# Development Server starten
python manage.py runserver

# In separatem Terminal:
# Database Check
python manage.py check

# Migration Check (für Model-Änderungen)
python manage.py makemigrations --dry-run
```

### 4. Code Quality Checks

```bash
# Django System Check
python manage.py check --deploy

# Code Linting (falls flake8 installiert)
python -m flake8 . --max-line-length=88

# Security Check (falls installiert)
python manage.py check --deploy
```

## VS Code Tasks und Shortcuts

### Vordefinierte Tasks (Cmd/Ctrl + Shift + P → "Tasks: Run Task"):

- **Django: Run Development Server** - Entwicklungsserver starten
- **Django: Run Tests** - Alle Tests ausführen
- **Django: Check Code** - Django System Check
- **Django: Migrate Database** - Migrations ausführen
- **Install Dependencies** - Requirements installieren
- **Lint Python Code** - Code-Qualität prüfen

### Debug Configurations (F5):

- **Django: Run Development Server** - Server mit Debugger
- **Django: Run Tests** - Tests mit Debugger
- **Django: Run Specific Test** - Spezifischen Test debuggen

## Review-Checkliste

### Code Review
- [ ] Code Style und Formatting korrekt
- [ ] Keine offensichtlichen Bugs oder Logic-Fehler
- [ ] Security Best Practices befolgt
- [ ] Performance-Implikationen betrachtet
- [ ] Error Handling angemessen

### Django-spezifisch
- [ ] Models: Richtige Field-Typen und Constraints
- [ ] Views: Proper Authentication/Authorization
- [ ] Templates: XSS-Schutz, korrekte Template-Tags
- [ ] URLs: Richtige Pattern und Naming
- [ ] Migrations: Rückwärts-kompatibel (falls möglich)

### Testing
- [ ] Alle Tests laufen durch
- [ ] Neue Features haben entsprechende Tests
- [ ] Bestehende Tests wurden nicht gebrochen
- [ ] Edge Cases sind abgedeckt

### Funktionalität
- [ ] Feature funktioniert wie erwartet
- [ ] UI/UX ist benutzerfreundlich
- [ ] Responsive Design (falls UI-Änderungen)
- [ ] Browser-Kompatibilität

## Kommentare und Feedback

### In VS Code (mit GitHub Extension):
1. Klicke auf "+" neben der Zeilennummer
2. Schreibe deinen Kommentar
3. Wähle "Single Comment" oder "Start Review"
4. Am Ende: "Finish Review" mit Approval/Changes/Comment

### Über GitHub Web Interface:
1. Navigiere zum PR auf GitHub
2. Gehe zum "Files changed" Tab
3. Hover über Zeilen und klicke "+" für Kommentare
4. Submit Review mit entsprechendem Status

## Häufige Probleme und Lösungen

### Python Interpreter nicht gefunden
```
Cmd/Ctrl + Shift + P → "Python: Select Interpreter" → venv/bin/python
```

### Django not found
```bash
# Virtual Environment aktivieren
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate     # Windows

# Dependencies neu installieren
pip install -r requirements.txt
```

### Tests schlagen fehl
```bash
# Database zurücksetzen (Development nur!)
rm db.sqlite3
python manage.py migrate
```

### VS Code erkennt Django nicht
- Stelle sicher, dass die Django Extension installiert ist
- Überprüfe die Python Interpreter-Einstellung
- Restart VS Code nach Extension-Installation

## Nützliche VS Code Shortcuts

- `Cmd/Ctrl + Shift + P` - Command Palette
- `Cmd/Ctrl + P` - Quick Open (Dateien)
- `F12` - Go to Definition
- `Alt/Opt + F12` - Peek Definition
- `Shift + F12` - Find All References
- `Cmd/Ctrl + F` - Find in File
- `Cmd/Ctrl + Shift + F` - Find in Files
- `F5` - Start Debugging
- `Cmd/Ctrl + F5` - Run Without Debugging

## Git Integration in VS Code

### Source Control Panel:
- Zeigt geänderte Dateien
- Stage/Unstage Änderungen
- Commit Messages schreiben
- Push/Pull/Sync

### GitLens Features:
- Blame Information inline
- Commit History
- Branch Comparison
- Repository Statistics

## Weitere Ressourcen

- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
- [VS Code Django Tutorial](https://code.visualstudio.com/docs/python/tutorial-django)
- [GitHub Pull Requests Extension](https://marketplace.visualstudio.com/items?itemName=GitHub.vscode-pull-request-github)
- [Django Documentation](https://docs.djangoproject.com/)
- [Git Tutorial](https://git-scm.com/docs/gittutorial)