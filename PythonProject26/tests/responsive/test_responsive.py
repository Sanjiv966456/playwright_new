"""Horizontal-overflow and viewport coverage."""

from __future__ import annotations

import pytest
from playwright.sync_api import expect


VIEWPORTS = [
    pytest.param({"width": 1920, "height": 1080}, id="desktop-1920"),
    pytest.param({"width": 1440, "height": 900}, id="desktop-1440"),
    pytest.param({"width": 768, "height": 1024}, id="tablet-768"),
    pytest.param({"width": 375, "height": 812}, id="mobile-375"),
    pytest.param({"width": 414, "height": 896}, id="mobile-414"),
]


@pytest.mark.responsive
@pytest.mark.parametrize("viewport_params", VIEWPORTS, indirect=True)
def test_homepage_has_no_horizontal_overflow(page, viewport_params, base_url: str) -> None:
    """The home layout fits within the viewport at standard breakpoints."""
    page.goto(base_url, wait_until="domcontentloaded")
    page.evaluate("document.fonts.ready")
    dimensions = page.evaluate(
        "() => ({viewport: document.documentElement.clientWidth, content: document.documentElement.scrollWidth})"
    )
    assert dimensions["content"] <= dimensions["viewport"], (
        f"Horizontal overflow at {viewport_params['width']}px: {dimensions}"
    )
    expect(page.get_by_role("main")).to_be_visible()
