from playwright.sync_api import Page

def test_check_box(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/")
    page.wait_for_timeout(10000)

    for day in ["Monday", "Saturday"]:
        checkbox= page.locator(f"input[value='{day}']")
        checkbox.check()