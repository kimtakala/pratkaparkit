# Final Submission Guide

## What is included

- Flask + SQLite app with user accounts, spots, classifications, comments, search, and profile pages
- CSRF protection and password hashing
- Custom HTML/CSS UI with labels, alt text, and preserved line breaks
- Automated tests in `tests/`
- The current layout uses `app.py`, `db/`, `users.py`, `items.py`, `comments.py`, `validation/`, `security/`, `errors/`, `templates/layout.html`, and `external/`

## How to run

```bash
source .venv/bin/activate
sqlite3 database.db < sql/init_db.sql
python app.py
```

## How to test

```bash
python -m unittest discover -s tests
```

## Rubric map

| Requirement | Evidence | Notes |
|---|---|---|
| User auth | `app.py`, `users.py`, `tests/test_auth_flow.py` | Register, login, logout |
| Spot CRUD | `app.py`, `items.py`, `tests/test_core_flow.py` | Create and view flow covered |
| Search | `app.py`, `items.py`, `tests/test_core_flow.py` | Query by title verified and bbox handled |
| User profile | `app.py`, `users.py`, `templates/user_profile.html` | Profile page and items list |
| Classifications | `items.py`, `sql/init_db.sql` | Many-to-many classification table |
| Comments | `app.py`, `comments.py`, `tests/test_core_flow.py` | Comment posting and display |
| Validation | `validation/`, `tests/test_validation_feedback.py` | Multiple errors and preserved input |
| UI/accessibility | `templates/layout.html`, `templates/`, `static/main.css` | Labels, alt text, line breaks |
| Pylint | `PYLINT_REPORT.md` | Final-report rationale included |

## Notes

- The project does not use JavaScript.
- The app is intended to be run directly from the repository root.