import pytest
from playwright.sync_api import Page,expect
def test_iframe(page: Page):
    page.goto("https://practice-automation.com/iframes/")
    page.locator("iframe[name=\"top-iframe\"]").content_frame.get_by_role("navigation", name="Main").click()
    page.locator("iframe[name=\"top-iframe\"]").content_frame.get_by_role("link", name="MCP", exact=True).click()
    page.wait_for_timeout(5000)

