from playwright.sync_api import Page, expect
def test_dashboard(logged_in_page):
    page = logged_in_page
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index")
    expect(page).to_have_title("OrangeHRM")
    expect(page.locator("h6")).to_have_text("Dashboard")

