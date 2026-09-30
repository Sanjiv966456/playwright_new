from playwright.sync_api import Page,expect

def test_select_india(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/")
    page.wait_for_timeout(5000)
    page.locator("#country").select_option("India")
    page.wait_for_timeout(5000)
    page.screenshot(path="country_selected.png",full_page=True)