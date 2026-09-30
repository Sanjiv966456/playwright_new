import pytest
from playwright.sync_api import Page, expect
from pathlib import Path


def test_downloadfile(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/p/download-files_25.html?m=1")
    page.wait_for_load_state('networkidle')
    
    # Try multiple selectors for the download button
    button = page.locator("button, input[type='button']").first
    
    with page.expect_download() as download_info:
        button.click()
    
    download = download_info.value
    download_path = Path.home() / "Downloads" / "test.txt"
    download.save_as(str(download_path))
    
    # Verify file exists
    assert download_path.exists(), f"Download failed: file not found at {download_path}"
