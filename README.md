# Binokel Score Tracker

A Django web application for tracking scores in the traditional Swabian card game Binokel.

## Features

- Track scores for 3-player Binokel games
- Record bid amounts, melds, and trick points
- Support for "abgehen" (going down) and "Durch" (taking all tricks)
- Track rounds won and determine the game winner

## Setup

### Development Environment

1. Clone the repository:
```bash
git clone https://github.com/LarsBerberich/Binokel-score-tracker.git
cd Binokel-score-tracker
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run database migrations:
```bash
python manage.py migrate
```

5. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

6. Start the development server:
```bash
python manage.py runserver
```

7. Open your browser and navigate to `http://localhost:8000`

### Using Docker

Alternatively, you can run the application using Docker:

```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`.

## Contributing

We welcome contributions to the Binokel Score Tracker! Here's how you can help:

### Finding Pull Requests to Review

Pull requests are available for review on GitHub:

1. **View all pull requests**: Visit [https://github.com/LarsBerberich/Binokel-score-tracker/pulls](https://github.com/LarsBerberich/Binokel-score-tracker/pulls)
2. **Filter by status**: 
   - Open PRs: [https://github.com/LarsBerberich/Binokel-score-tracker/pulls?q=is%3Aopen](https://github.com/LarsBerberich/Binokel-score-tracker/pulls?q=is%3Aopen)
   - Draft PRs: [https://github.com/LarsBerberich/Binokel-score-tracker/pulls?q=is%3Adraft](https://github.com/LarsBerberich/Binokel-score-tracker/pulls?q=is%3Adraft)
3. **Review requested**: Check for PRs where your review has been specifically requested

### How to Review a Pull Request

1. Click on any pull request from the list
2. Review the **Files changed** tab to see the code changes
3. Add comments on specific lines by clicking the "+" icon
4. Use the **Review changes** button to:
   - **Comment**: Add general feedback
   - **Approve**: Approve the changes
   - **Request changes**: Request modifications before merging

### How to Contribute

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** and commit them
4. **Push to your fork**: `git push origin feature/your-feature-name`
5. **Create a Pull Request** from your fork to the main repository

### Development Guidelines

- Follow Django best practices
- Write tests for new features
- Update documentation as needed
- Use meaningful commit messages
- Ensure all tests pass before submitting a PR

### Running Tests

```bash
python manage.py test
```

For behavior-driven development tests:
```bash
python manage.py behave
```

## Project Structure

```
Binokel-score-tracker/
├── binokel_project/          # Django project settings
├── score_tracker/            # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── forms.py             # Django forms
│   └── migrations/          # Database migrations
├── templates/               # HTML templates
├── static/                  # Static files (CSS, JS, images)
├── requirements.txt         # Python dependencies
├── manage.py               # Django management script
└── README.md               # This file
```

## License

This project is open source. Please check the repository for license details.

## Support

If you encounter any issues or have questions:

1. Check the [Issues page](https://github.com/LarsBerberich/Binokel-score-tracker/issues)
2. Create a new issue if your problem isn't already reported
3. For pull request discussions, use the PR comment system