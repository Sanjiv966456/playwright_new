# AGENTS: How to be productive in this workspace

Checklist for an AI coding agent
- Understand there are two small Playwright projects under the workspace root: `pythonProjectplaywright/` and `playwright/`.
- Primary automation code and tests live in `pythonProjectplaywright/` (see examples below).
- Use the exact file examples and run commands listed in the "Quick actions" section before making changes.

Quick architecture & purpose
- This workspace is test/automation-focused and uses Playwright (both sync and async APIs).
  - `pythonProjectplaywright/contact_form_filler.py` — an async Playwright script that fills and screenshots a contact form.
  - `pythonProjectplaywright/test_checkbox.py` — a small sync Playwright script/test that navigates DemoQA and manipulates checkboxes.
  - `pythonProjectplaywright/pwright/` — contains pytest tests and a `pytest.ini` (Allure results configured).

Key patterns and conventions (from the code)
- Mixed sync and async Playwright usage in the same project:
  - Async example: `contact_form_filler.py` uses `async_playwright` and `asyncio.run(...)`.
  - Sync example: tests in `pwright/` and `test_checkbox.py` use `sync_playwright()` or `Page` fixtures.
  Agents should not refactor sync -> async automatically; preserve the calling style of each file.

- Browser startup and visibility: many scripts launch browsers with chromium and headless=False (explicit). Examples:
  - contact_form_filler.py: `await p.chromium.launch(headless=False)`
  - test_checkbox.py: `playwright.chromium.launch(headless=False)`
  So expect interactive/test debugging mode by default.

- Selectors and resilience patterns:
  - contact_form_filler.py prefers flexible selectors (multiple attribute alternatives) and fallback queries. Example:
    page.query_selector('input[name="name"], [placeholder*="Name"], [placeholder*="name"]')
  - Tests often use explicit waits like `page.wait_for_timeout(10000)` or `time.sleep(2)` — preserve these when reproducing behavior unless improving flakiness.

- Artifacts and diagnostics:
  - Scripts save screenshots: `contact_form_filled.png`, `contact_form_submitted.png`, and `error_screenshot.png`.
  - Tests / pytest.ini are configured to write Allure results to `allure-results` (see `pythonProjectplaywright/pwright/pytest.ini`).

Critical developer workflows (how to run things)
- Run the contact form script (from project root):
  PowerShell:
    cd pythonProjectplaywright; python .\contact_form_filler.py

- Run a single sync Playwright script (example):
  PowerShell:
    cd pythonProjectplaywright; python .\test_checkbox.py

- Run pytest for tests in `pwright/` (pytest.ini sets testpaths = tests which does NOT match `pwright/`). Two options:
  - Run pytest pointing at the `pwright` directory explicitly:
      cd pythonProjectplaywright; pytest pwright -v
  - Or move/adjust tests to a `tests/` dir or update `pytest.ini` if you change test layout.

- Ensure dependencies are installed (Playwright + test extras). Minimal commands (PowerShell):
  python -m pip install playwright pytest allure-pytest
  python -m playwright install  # installs browser binaries

Integration points & external dependencies
- Playwright (python package + installed browser binaries) — required to run any script or test.
- allure-pytest is referenced in tests and `pytest.ini` (Allure result directory configured). Viewing reports requires an Allure CLI or other reporter.

Project-specific pitfalls for agents
- Do NOT convert sync tests to asyncio without running the tests — the repo intentionally mixes both APIs.
- Tests rely on explicit sleeps and long timeouts; removing them will change runtime behaviour and may hide why authors added them.
- `pytest.ini` currently points tests to `tests/` but the existing test module folder is `pwright/` — if adding tests, follow the current layout (`pwright/`) or update `pytest.ini` accordingly.

Files to inspect when changing behavior
- `pythonProjectplaywright/contact_form_filler.py` — core example of how forms are filled, fallback selectors, screenshots.
- `pythonProjectplaywright/test_checkbox.py` — standalone script illustrating sync_playwright usage and manual invocation.
- `pythonProjectplaywright/pwright/pytest.ini` — test runner flags (Allure output, verbosity).

If you need to make changes
- Run the script or test locally first (commands above) to reproduce behavior and gather screenshots/traces.
- When modifying tests, update `pytest.ini` or the `pwright/` path so pytest discovers tests (avoid surprise test discovery breakages).

Contact / next steps
- If you want, I can:
  - Add a small `requirements.txt` and a runnable `run-tests.ps1` wrapper that installs deps and runs pytest in the correct folder.
  - Fix `pytest.ini` testpaths to include `pwright/`.

