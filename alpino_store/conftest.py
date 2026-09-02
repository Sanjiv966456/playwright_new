import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def page():
    """Fixture to provide a Playwright page for tests"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        yield page
        browser.close()
