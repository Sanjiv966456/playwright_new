import pytest
from playwright.sync_api import Page, expect

def test_select_weekdays_sequentially(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/")
    page.wait_for_timeout(5000)
    
    # Uncheck all days first
    page.locator('input[value="sunday"]').uncheck(force=True)
    page.locator('input[value="monday"]').uncheck(force=True)
    page.locator('input[value="tuesday"]').uncheck(force=True)
    page.locator('input[value="wednesday"]').uncheck(force=True)
    page.locator('input[value="thursday"]').uncheck(force=True)
    page.locator('input[value="friday"]').uncheck(force=True)
    page.locator('input[value="saturday"]').uncheck(force=True)
    
    page.wait_for_timeout(2000)
    
    # Select Monday
    page.locator('input[value="monday"]').check()
    page.wait_for_timeout(2000)
    page.screenshot(path="monday_selected.png")
    
    # Select Tuesday
    page.locator('input[value="tuesday"]').check()
    page.wait_for_timeout(2000)
    page.screenshot(path="monday_tuesday_selected.png")
    
    # Select Wednesday
    page.locator('input[value="wednesday"]').check()
    page.wait_for_timeout(2000)
    page.screenshot(path="all_weekdays_selected.png")