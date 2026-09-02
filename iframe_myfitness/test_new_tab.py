import re
from playwright.sync_api import Page, expect


def test_new_tab(page:Page):
    page.goto("https://practice-automation.com/window-operations/")
    with page.expect_popup() as page1_info:
        page.get_by_role("button", name="New Tab").click()
    page1 = page1_info.value

    # ---------------------
