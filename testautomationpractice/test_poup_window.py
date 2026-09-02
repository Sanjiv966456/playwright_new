import pytest
from playwright.sync_api import Page,expect
def test_pop_up(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/")
    with page.expect_popup() as page2_info:
        page.get_by_role("button", name="Popup Windows").click()
    page2 = page2_info.value