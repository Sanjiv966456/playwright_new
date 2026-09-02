import os
from playwright.sync_api import sync_playwright


def download_file(headless=False):
    url = "https://testautomationpractice.blogspot.com/p/download-files_25.html"
    downloads_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(downloads_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(url)

        # Trigger the download and wait for it
        with page.expect_download() as download_info:
            page.get_by_role("button", name="Generate and Download Text File").click()

        download = download_info.value
        filename = download.suggested_filename or "downloaded_file.txt"
        target = os.path.join(downloads_dir, filename)
        download.save_as(target)

        print(f"Saved download to: {target}")
        browser.close()


if __name__ == "__main__":
    download_file(headless=False)
