import re
import allure
from playwright.sync_api import Playwright, sync_playwright, expect


@allure.title("DemoQA Checkbox Selection Test")
@allure.description("Test selecting and deselecting checkboxes on DemoQA")
@allure.severity(allure.severity_level.CRITICAL)
def test_run(playwright: Playwright) -> None:
    """Test checkbox selection functionality"""
    
    with allure.step("Launch chromium browser"):
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
    
    with allure.step("Navigate to DemoQA checkbox page"):
        page.goto("https://demoqa.com/checkbox")
        page.wait_for_timeout(10000)
    
    with allure.step("Expand the tree by clicking switcher"):
        page.locator(".rc-tree-switcher").click()
        page.wait_for_timeout(2000)
    
    with allure.step("Select 'Home' checkbox"):
        page.get_by_role("checkbox", name="Select Home").click()
        page.wait_for_timeout(10000)
    
    with allure.step("Deselect 'Home' checkbox"):
        page.get_by_role("checkbox", name="Select Home").click()
        page.wait_for_timeout(10000)
    
    with allure.step("Take final screenshot"):
        page.screenshot(path="checkbox_test.png")
    
    with allure.step("Close browser"):
        context.close()
        browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_run(playwright)
