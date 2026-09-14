"""Test-specific fixture overrides."""

from __future__ import annotations

from typing import Generator

import pytest
from playwright.sync_api import Browser, Playwright


@pytest.fixture
def browser(playwright: Playwright, browser_name: str) -> Generator[Browser, None, None]:
    """Override browser fixture to run product listing tests in headed mode."""
    browser_type = getattr(playwright, browser_name)
    instance = browser_type.launch(headless=False)
    yield instance
    instance.close()
