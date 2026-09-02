import pytest
from playwright.sync_api import Page, expect

def test_select_scrolling_dropdown(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/p/playwrightpractice.html")
    drop_down = page.locator("select")
    drop_down.scroll_into_view_if_needed()
    drop_down.select_option(label="Item 112")
    expect(drop_down).to_have_value("Item 112")
    page.screenshot(path="item112_selected.png")
    print("✓ Item 112 selected successfully!")
    print(f"Selected value: {drop_down.evaluate('el => el.value')}")
    page.wait_for_timeout(2000)

