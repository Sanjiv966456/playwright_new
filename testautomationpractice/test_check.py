import pytest
from playwright.sync_api import Page,expect
def test_check(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/")
    page.wait_for_timeout(5000)
    page.locator('#male').click()
    page.wait_for_timeout(5000)
    page.locator('#female').click()
    page.wait_for_timeout(5000)