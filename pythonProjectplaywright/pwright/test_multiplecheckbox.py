from playwright.sync_api import Page

def test_check_box(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/")

    for checkbox in page.locator("input[type='checkbox']").all():
        checkbox.scroll_into_view_if_needed()
        checkbox.check()
