import os
import re
import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "https://heatingandcoolingfixer.com.au"
PAGES = ["/", "/about/", "/careers/"]
PHONE_VARIANTS = [
    "1800 548 492",
    "1800548492",
    "1800-548-492",
    "(1800) 548 492",
]

SCREENSHOT_DIR = Path("screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)


def page_has_phone(content: str) -> bool:
    # normalize and check multiple formats
    for v in PHONE_VARIANTS:
        if v in content:
            return True
    # digits-only check
    digits = re.sub(r"\D", "", content)
    if "1800548492" in digits:
        return True
    return False


@pytest.mark.parametrize("path", PAGES)
def test_phone_present_on_page(path):
    url = BASE.rstrip("/") + path

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url, wait_until="load", timeout=30000)
        # small wait for dynamic content
        page.wait_for_timeout(1000)
        content = page.content()

        # save screenshot
        safe_name = path.strip("/") or "home"
        safe_name = safe_name.replace("/", "_") or "home"
        screenshot_path = SCREENSHOT_DIR / f"{safe_name}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)

        assert page_has_phone(content), f"Phone number not found on {url}. Screenshot saved to {screenshot_path}"

        context.close()
        browser.close()
