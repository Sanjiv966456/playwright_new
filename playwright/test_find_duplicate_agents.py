"""
Marriott Lane Property Form Automation Script
Fills the "Find A Property Near Me" form at https://marriottlaneco.wpenginepowered.com/areas/
with dummy test data using Playwright
"""

import asyncio
from playwright.async_api import async_playwright
import time


async def fill_property_form():
    """Fill the property inquiry form with dummy data"""

    # Dummy test data
    form_data = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "phone": "02 9906 2300",
        "suburb": "5555",
        "message": "I am interested in finding a property in this area. Please provide more information about available listings."
    }

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        try:
            # Navigate to areas page
            print("Navigating to Marriott Lane areas page...")
            await page.goto("https://marriottlaneco.wpenginepowered.com/areas/",
                          wait_until="networkidle")

            # Wait for page to load completely
            await page.wait_for_load_state("domcontentloaded")
            time.sleep(2)

            print("Page loaded successfully!")

            # Fill Name field
            print("Filling in name field...")
            await page.fill('input[placeholder*="Name"]', form_data["name"])
            print(f"✓ Name filled: {form_data['name']}")

            # Fill Email field
            print("Filling in email field...")
            await page.fill('input[placeholder*="example@gmail.com.au"]', form_data["email"])
            print(f"✓ Email filled: {form_data['email']}")

            # Fill Phone Number field
            print("Filling in phone number field...")
            await page.fill('input[placeholder*="00 0000 0000"]', form_data["phone"])
            print(f"✓ Phone filled: {form_data['phone']}")

            # Fill Suburb field
            print("Filling in suburb field...")
            await page.fill('input[placeholder*="5555"]', form_data["suburb"])
            print(f"✓ Suburb filled: {form_data['suburb']}")

            # Fill Message field
            print("Filling in message field...")
            await page.fill('textarea', form_data["message"])
            print(f"✓ Message filled: {form_data['message'][:50]}...")

            # Take screenshot before submission
            print("Taking screenshot of filled form...")
            await page.screenshot(path="property_form_filled.png")
            print("✓ Screenshot saved: property_form_filled.png")

            # Find and click SUBMIT button
            print("Looking for submit button...")
            submit_button = await page.query_selector('button:has-text("SUBMIT")')

            if submit_button:
                print("Clicking submit button...")
                await submit_button.click()

                # Wait for submission
                await page.wait_for_load_state("networkidle")
                time.sleep(2)

                # Take final screenshot
                await page.screenshot(path="property_form_submitted.png")
                print("✓ Form submitted successfully!")
                print("✓ Screenshot saved: property_form_submitted.png")
            else:
                print("⚠ Submit button not found")

        except Exception as e:
            print(f"❌ Error occurred: {str(e)}")
            await page.screenshot(path="error_screenshot.png")
            print("Error screenshot saved: error_screenshot.png")

        finally:
            # Close browser
            await browser.close()
            print("Browser closed.")


if __name__ == "__main__":
    print("Starting Property Form Automation...")
    print("=" * 50)
    asyncio.run(fill_property_form())
    print("=" * 50)
    print("Script completed!")