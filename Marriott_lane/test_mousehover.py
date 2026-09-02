import pytest
from playwright.sync_api import Page, expect

def test_Mouse_hover(page: Page):
    page.goto("https://marriottlaneco.wpenginepowered.com/")
    page.wait_for_load_state("networkidle")
    page.get_by_role("link", name="Property Management", exact=True).hover()
    page.get_by_role("link", name="Property Management Services").click()
    page.wait_for_timeout(3000)