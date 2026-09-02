import pytest
from playwright.sync_api import Page, expect
def test_searh(page: Page):
    page.goto("https://eurodiesel.wpenginepowered.com/")
    page.wait_for_load_state("networkidle")
    page.get_by_role("textbox", name="Search For Product").click()
    page.get_by_role("textbox", name="Search For Product").fill("hatz")
    page.get_by_role("button", name="Submit").click()
    page.wait_for_timeout(5000)
    page.close()