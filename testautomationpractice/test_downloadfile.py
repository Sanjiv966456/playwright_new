import pytest
from playwright.sync_api import Page,expect
def test_downloadfile(page:Page):
    page.goto("https://testautomationpractice.blogspot.com/p/download-files_25.html?m=1")
    with page.expect_download() as download_info:
        page.get_by_role("button", name="Generate and Download Text").click()
    download = download_info.value
    download.save_as("C:/Users/HP/Downloads/test.txt")