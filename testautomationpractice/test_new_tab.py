import pytest
from playwright.sync_api import Page,expect
def test_new_tab(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/")

    with page.expect_popup() as page1_info:
        page.get_by_role("button", name="New Tab").click()
    page1 = page1_info.value
    page1.wait_for_load_state()
    inner_test = page1.inner_text("h1")
    print(inner_test)
