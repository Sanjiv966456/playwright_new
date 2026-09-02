import pytest
from playwright.sync_api import Page, expect
def test_download(page:Page):
    page.goto("https://practice-automation.com/file-download/")
    with page.expect_download() as download_info:
        page.get_by_role("link", name="Download").nth(1).click()
    download = download_info.value
    page.wait_for_timeout()
