from playwright.sync_api import Page, expect

def test_logo_capture(page: Page):
    """Test to verify Alpino Health Foods logo is visible and capture screenshot"""
    page.goto("https://alpino.store/", wait_until="load")
    page.wait_for_timeout(3000)
    
    # Close popup
    try:
        close_button = page.locator("#iframe-kp").content_frame.locator("#desktop_close_button")
        if close_button.is_visible():
            close_button.click()
            page.wait_for_timeout(500)
    except Exception as e:
        print(f"Could not close popup: {e}")
    
    # Wait for logo to be visible
    page.wait_for_timeout(1000)
    
    # Get logo - use first visible one since there are multiple
    try:
        logo = page.locator("header img[alt='Alpino Health Foods']")
        print(f"Logo found: {logo}")
        expect(logo).to_be_visible()
    except Exception as e:
        print(f"Logo not found with header selector, trying main logo: {e}")
        # Fallback: try the main logo (larger one)
        logo = page.locator("img[alt='Alpino Health Foods'][width='595']").first
        expect(logo).to_be_visible()
    
    logo.screenshot(path="logo.png")
    page.wait_for_timeout(2000)
