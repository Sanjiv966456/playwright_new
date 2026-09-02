import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture
def browser_setup():
    """Setup and teardown browser for each test"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        yield page
        browser.close()


class TestGetQuote:
    """Test suite for McKinnon Heat electric heat pump quote functionality"""
    
    def test_click_get_a_free_quote_button_main(self, browser_setup):
        """Test clicking the 'Get a Free Quote' button in the main header"""
        page = browser_setup
        
        # Navigate to the product page
        page.goto("https://mckinnonheadev.wpenginepowered.com/product-category/cooling/electric-heat-pump/")
        
        # Wait for page to fully load
        page.wait_for_load_state("networkidle")
        
        # Use the specific ID locator for the quote button in the header
        # This is the most reliable way to target the correct button
        quote_button = page.locator("#quoteModalTrigger").first
        
        # Verify the button exists and is visible
        assert quote_button.is_visible(), "Get a Free Quote button should be visible"
        assert quote_button.is_enabled(), "Get a Free Quote button should be enabled"
        
        # Click the button
        quote_button.click()
        
        # Wait for modal or action to complete
        page.wait_for_timeout(2000)
        
        # Take screenshot for verification
        page.screenshot(path="quote_button_clicked.png")
        
        print("[PASS] Successfully clicked 'Get a Free Quote' button")
        print(f"[INFO] Current URL: {page.url}")
    
    def test_get_a_free_quote_button_properties(self, browser_setup):
        """Test that the 'Get a Free Quote' button has correct properties"""
        page = browser_setup
        
        # Navigate to the product page
        page.goto("https://mckinnonheadev.wpenginepowered.com/product-category/cooling/electric-heat-pump/")
        
        # Wait for page to fully load
        page.wait_for_load_state("networkidle")
        
        # Get the main quote button by ID
        quote_button = page.locator("#quoteModalTrigger").first
        
        # Verify button is visible
        assert quote_button.is_visible(), "Button should be visible"
        
        # Verify button is enabled
        assert quote_button.is_enabled(), "Button should be enabled"
        
        # Get button bounds to verify it's in viewport
        box = quote_button.bounding_box()
        assert box is not None, "Button should have a valid bounding box"
        assert box['width'] > 0 and box['height'] > 0, "Button should have valid dimensions"
        
        # Verify button has correct text
        button_text = quote_button.text_content()
        assert "Get a Free Quote" in button_text, "Button should contain 'Get a Free Quote' text"
        
        # Hover over button to verify interactivity
        quote_button.hover()
        page.wait_for_timeout(500)
        
        print(f"[PASS] Button is visible and clickable at position: {box}")
        print(f"[INFO] Button dimensions: {box['width']}x{box['height']}")
        print(f"[INFO] Button text: {button_text.strip()}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
