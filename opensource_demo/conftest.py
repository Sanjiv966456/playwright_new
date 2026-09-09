import pytest
from playwright.sync_api import Page,expect

@pytest.fixture()
def logged_in_page(page: Page):
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    page.get_by_placeholder("Username").fill("Admin")
    page.get_by_placeholder("Password").fill("admin123")
    page.get_by_role("button", name="Login").click()
    page.wait_for_url("**/dashboard/index")
    expect(page).to_have_url("https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index")
    yield page