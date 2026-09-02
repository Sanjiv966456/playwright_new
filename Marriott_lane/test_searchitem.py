import pytest
from playwright.sync_api import Page,expect
def test_search_item(page: Page):
    page.goto("https://marriottlaneco.wpenginepowered.com/rent/")
    page.wait_for_load_state("networkidle")
    page.locator("[name='s']").fill("pacific")
    page.wait_for_timeout(2000)
    page.locator("[name='listing_type']").select_option("rent")
    page.get_by_role("button", name="Search").click()
    page.wait_for_timeout(3000)