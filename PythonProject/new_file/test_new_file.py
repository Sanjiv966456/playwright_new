import re
from playwright.sync_api import Playwright, sync_playwright, expect


def test_run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://demoqa.com/checkbox")
    page.wait_for_timeout(10000)
    page.locator(".rc-tree-switcher").click()
    page.get_by_role("checkbox", name="Select Home").click()
    page.wait_for_timeout(10000)
    page.get_by_role("checkbox", name="Select Home").click()
    page.wait_for_timeout(10000)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    test_run(playwright)