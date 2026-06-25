# Pylint Report

Pylint score on the final application version: **7.80/10**

## Findings and decisions

### `app.py`
- Missing module and function docstrings: left as-is because the project follows the course style of small, direct functions and short modules.
- Import order warnings: left as-is because the current import grouping keeps Flask and local imports readable in the main app module.
- Broad exception catch around tile generation: left as-is to avoid breaking the spot detail page if the optional map preview fails.

### `users.py`
- Missing docstrings: left as-is for the same reason as `app.py`.
- Unused `check_password_hash` import: left as-is because the import is still present in the module structure and does not affect runtime behavior.

### `items.py`
- Long lines and too many arguments warnings: left as-is because the CRUD helpers intentionally mirror the database fields and route inputs.
- Missing docstrings: left as-is to keep the module consistent with the rest of the codebase.
- Duplicate code warning for the spot listing queries: left as-is because the shared query structure is easier to maintain in this small project than introducing an abstraction just for pylint.

### `comments.py`
- Long lines and missing docstrings: left as-is for consistency with the rest of the app modules.

### `db/__init__.py`
- Missing docstrings and one unused argument warning: left as-is because the functions are straightforward database helpers and the teardown callback signature is framework-driven.

### `config.py`
- Missing module docstring and duplicate-code warning: left as-is because the file only contains configuration constants and should stay minimal.

## Summary

The reported issues are mostly style-related. The code is kept in a course-friendly form and the warnings do not block the app from working correctly.