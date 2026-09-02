# Playwright + pytest test suite for marriottlaneco

This project contains Playwright Python tests with a Page Object Model for https://marriottlaneco.wpenginepowered.com/

Setup (PowerShell):

```powershell
python -m pip install -r requirements.txt ;
python -m playwright install
```

Run tests (headless):

```powershell
pytest -q
```

Artifacts (screenshots/videos) are saved to `artifacts/screenshots` and `artifacts/videos` by default.

Files added:
- `tests/conftest.py` — fixtures and artifact capture
- `tests/pages/*.py` — page object model classes
- `tests/test_*.py` — high-level tests


