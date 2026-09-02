import os
import argparse
from playwright.sync_api import sync_playwright


def download_from_url(url: str, headless: bool = False, timeout: int = 30000):
    downloads_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(downloads_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        page.goto(url)

        # Try several locators to trigger the download (mobile/desktop variants differ)
        with page.expect_download(timeout=timeout) as download_info:
            tried = False
            try:
                page.get_by_role("button", name="Generate and Download Text File").click()
                tried = True
            except Exception:
                try:
                    page.get_by_text("Generate and Download Text File").first.click()
                    tried = True
                except Exception:
                    try:
                        page.click("#download-text-file")
                        tried = True
                    except Exception:
                        # fallback: click the first button that contains the word 'download'
                        try:
                            buttons = page.locator('button')
                            for i in range(buttons.count()):
                                text = buttons.nth(i).inner_text().lower()
                                if 'download' in text or 'generate' in text:
                                    buttons.nth(i).click()
                                    tried = True
                                    break
                        except Exception:
                            pass

            if not tried:
                # If no click happened, raise so expect_download times out and we can report
                raise RuntimeError("Could not find a download trigger on the page")

        download = download_info.value
        filename = download.suggested_filename or "downloaded_file"
        target = os.path.join(downloads_dir, filename)
        download.save_as(target)

        print(f"Saved download to: {target}")
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download generated file from TestAutomationPractice page")
    parser.add_argument("--url", default="https://testautomationpractice.blogspot.com/p/download-files_25.html?m=1", help="Page URL")
    parser.add_argument("--headless", action="store_true", help="Run browser headless")
    args = parser.parse_args()
    download_from_url(args.url, headless=args.headless)
