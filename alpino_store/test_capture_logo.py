import pytest
from playwright.sync_api import Page,expect
def test_logo_capture(page:Page):
    page.goto("https://alpino.store/")
    page.wait_for_timeout(10000)
    #close popup
    page.locator("#iframe-kp").content_frame.locator("#desktop_close_button").click()
    logo = page.locator("img[alt*='Alpino' i], a[class*='logo' i] img, img[class*='logo' i]").first
    expect(logo).to_be_visible()
    logo.screenshot(path="logo.png")
    page.wait_for_timeout(2000)