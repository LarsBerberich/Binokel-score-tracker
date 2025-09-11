# 🎯 Pull Request Review Guide - Quick Start

**Schnellanleitung für Pull Request Reviews in VS Code**

## ⚡ Schnellstart (5 Minuten)

### 1. Repository Setup
```bash
git clone https://github.com/LarsBerberich/Binokel-score-tracker.git
cd Binokel-score-tracker
code .  # VS Code öffnen
```

### 2. VS Code Extensions installieren
VS Code wird automatisch die benötigten Extensions vorschlagen. Wichtigste:
- **GitHub Pull Requests** (für direkten PR-Zugriff)
- **Python** (für Django-Entwicklung) 
- **GitLens** (für Git-Integration)

### 3. Python Environment
```bash
# Virtual Environment erstellen und aktivieren
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder: venv\Scripts\activate  # Windows

# Dependencies installieren
pip install -r requirements.txt

# Django Setup
python manage.py migrate
python manage.py check
```

### 4. Pull Request auschecken

**Option A - GitHub Extension (Empfohlen):**
1. GitHub Panel öffnen (Seitenleiste)
2. "Pull Requests" → PR auswählen
3. "Checkout" klicken

**Option B - Kommandozeile:**
```bash
git fetch origin
git checkout -b review-branch origin/pr-branch-name
```

### 5. Code Review
1. **Änderungen ansehen**: GitHub Panel → "Changes"
2. **Tests ausführen**: `python manage.py test`
3. **Server testen**: `python manage.py runserver`
4. **Kommentare hinzufügen**: "+" neben Zeilennummern

## 📚 Detaillierte Guides

- **[VS_CODE_REVIEW_GUIDE.md](VS_CODE_REVIEW_GUIDE.md)** - Vollständige VS Code Anleitung
- **[REVIEW_CHECKLIST.md](REVIEW_CHECKLIST.md)** - Review Checkliste
- **Setup Scripts**: `setup_dev.sh` (Linux/Mac) oder `setup_dev.bat` (Windows)

## 🚀 VS Code Features

### Debugging
- **F5**: Django Development Server mit Debugger starten
- **Breakpoints**: Klick links neben Zeilennummern
- **Debug Console**: Variablen untersuchen

### Testing  
- **Test Panel**: Tests direkt in VS Code ausführen
- **Tasks**: `Cmd/Ctrl + Shift + P` → "Tasks: Run Task"
  - "Django: Run Tests"
  - "Django: Run Development Server"

### Git Integration
- **Source Control Panel**: Änderungen verwalten
- **GitLens**: Inline Git-Informationen
- **Git Graph**: Visueller Git-Verlauf

## ✅ Review Checkliste (Essentials)

### Code
- [ ] Tests laufen durch: `python manage.py test`
- [ ] Django Check OK: `python manage.py check`
- [ ] Code Style befolgt Django-Konventionen
- [ ] Keine offensichtlichen Security-Issues

### Binokel-spezifisch
- [ ] Scoring-Logic ist korrekt (Meldungen, Stiche, Bid)
- [ ] Game Flow funktioniert (Runden, Spielende)
- [ ] UI ist benutzerfreundlich

### Tests
```bash
# Alle Tests
python manage.py test --verbosity=2

# Spezifische Tests
python manage.py test score_tracker.tests.GameModelTest

# Development Server
python manage.py runserver
```

## 🎮 Typische Review-Szenarien

### Model-Änderungen
1. Migration prüfen: `python manage.py makemigrations --dry-run`
2. Backward-Compatibility testen
3. Model-Tests ausführen

### View-Änderungen
1. URL-Routing testen
2. Template-Integration prüfen
3. HTTP Status Codes validieren

### Frontend-Änderungen
1. Browser öffnen: `http://localhost:8000`
2. Responsive Design testen
3. User Experience bewerten

## 💡 Pro Tips

### VS Code Shortcuts
- `Cmd/Ctrl + P`: Datei schnell öffnen
- `F12`: Go to Definition
- `Shift + F12`: Find References
- `Cmd/Ctrl + Shift + F`: In allen Dateien suchen

### Django Commands
```bash
# Interaktive Shell
python manage.py shell

# Database Admin
python manage.py dbshell

# Static Files
python manage.py collectstatic
```

### Git Commands
```bash
# Änderungen vergleichen
git diff main...HEAD

# Commit History
git log main..HEAD --oneline

# Geänderte Dateien
git diff --name-only main...HEAD
```

## 🆘 Troubleshooting

### "Django not found"
```bash
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### "Python interpreter not found"
`Cmd/Ctrl + Shift + P` → "Python: Select Interpreter" → `venv/bin/python`

### Tests schlagen fehl
```bash
rm db.sqlite3  # Reset Database
python manage.py migrate
python manage.py test
```

### VS Code Extensions fehlen
`Cmd/Ctrl + Shift + P` → "Extensions: Show Recommended Extensions"

---

**Happy Reviewing! 🎉**

Für weitere Fragen oder Probleme, siehe die detaillierte Dokumentation in den anderen Markdown-Dateien.