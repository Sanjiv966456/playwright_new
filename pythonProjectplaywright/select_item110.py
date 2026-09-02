"""
Simple script to open the Playwright practice page and select "Item 110"

Usage (PowerShell, from project root):
  cd pythonProjectplaywright; python .\\select_item110.py

This script uses the synchronous Playwright API and launches a visible
Chromium browser (headless=False) so you can watch the selection happen.
"""
from playwright.sync_api import sync_playwright
import time

URL = "https://testautomationpractice.blogspot.com/p/playwrightpractice.html"
TARGET_LABEL = "Item 110"


def select_scrolling_dropdown_item(label: str = TARGET_LABEL) -> bool:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            print(f"Navigating to {URL} ...")
            page.goto(URL, wait_until="networkidle")
            # Give the page a moment to render (matches project patterns)
            page.wait_for_load_state("domcontentloaded")
            time.sleep(1)

            # Find all <select> elements and look for one that contains the target label
            selects = page.locator("select")
            count = selects.count()
            print(f"Found {count} <select> element(s) on the page")

            for i in range(count):
                sel = selects.nth(i)
                # Get option texts via evaluation to avoid coupling to Playwright helpers
                option_texts = sel.evaluate("el => Array.from(el.options).map(o => o.text).map(t => t.trim())")
                # option_texts is a Python list of strings
                print(f"Select #{i} options preview: {option_texts[:5]}")
                if label in option_texts:
                    print(f"Selecting '{label}' in select #{i} ...")
                    sel.select_option(label=label)
                    # small pause to allow UI update
                    time.sleep(1)
                    screenshot = f"selected_{label.replace(' ', '_')}.png"
                    page.screenshot(path=screenshot)
                    print(f"✓ Screenshot saved: {screenshot}")
                    # verify selection
                    selected_value = sel.evaluate("el => el.value")
                    print(f"Selected value attribute: '{selected_value}'")
                    browser.close()
                    return True

            print(f"⚠ Could not find an option with label '{label}' in any <select> on the page")
            # Take a diagnostic screenshot
            page.screenshot(path="select_item_not_found.png")
            browser.close()
            return False

        except Exception as e:
            print(f"❌ Error while running script: {e}")
            try:
                page.screenshot(path="select_item_error.png")
                print("Saved error screenshot: select_item_error.png")
            except Exception:
                pass
            browser.close()
            return False


if __name__ == "__main__":
    print("Starting select_item110 script")
    print("=" * 50)
    ok = select_scrolling_dropdown_item()
    if ok:
        print("Done: item selected")
    else:
        print("Done: item not selected or an error occurred")
    print("=" * 50)

