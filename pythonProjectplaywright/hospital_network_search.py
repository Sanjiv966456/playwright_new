"""
Hospital Network Search Automation Script
Fills the hospital search form at https://rules.nivabupa.com/hospital-network/
with location, hospital, and treatment data using Playwright
"""

import asyncio
from playwright.async_api import async_playwright
import time


async def search_hospital_network():
    """Fill the hospital network search form and search"""

    # Search criteria
    search_data = {
        "location": "Vadodara",
        "hospital": "Sterling Hospital",
        "treatment": "Eye"
    }

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)  # Set to True for headless mode
        page = await browser.new_page()

        try:
            # Navigate to hospital network page
            print("Navigating to hospital network page...")
            await page.goto("https://rules.nivabupa.com/hospital-network/",
                          wait_until="networkidle")

            # Wait for page to load completely
            await page.wait_for_load_state("domcontentloaded")
            time.sleep(2)

            print("Page loaded successfully!")

            # Fill Location field
            print("Filling in location field...")
            location_field = await page.query_selector(
                'input[name="location"], input[placeholder*="Location"], input[placeholder*="location"], '
                'input[name="city"], input[placeholder*="City"]'
            )
            if location_field:
                await location_field.fill(search_data["location"])
                print(f"✓ Location filled: {search_data['location']}")
                time.sleep(1)
            else:
                print("⚠ Location field not found, trying alternative selectors...")
                try:
                    await page.fill('input:first-of-type', search_data["location"])
                    print(f"✓ Location filled using alternative method: {search_data['location']}")
                except Exception as e:
                    print(f"⚠ Location field could not be filled: {str(e)}")

            # Fill Hospital field
            print("Filling in hospital field...")
            hospital_field = await page.query_selector(
                'input[name="hospital"], input[placeholder*="Hospital"], input[placeholder*="hospital"], '
                'input[name="hospital_name"], input[placeholder*="Hospital Name"]'
            )
            if hospital_field:
                await hospital_field.fill(search_data["hospital"])
                print(f"✓ Hospital filled: {search_data['hospital']}")
                time.sleep(1)
            else:
                print("⚠ Hospital field not found, trying alternative selectors...")
                try:
                    inputs = await page.query_selector_all('input[type="text"]')
                    if len(inputs) >= 2:
                        await inputs[1].fill(search_data["hospital"])
                        print(f"✓ Hospital filled using alternative method: {search_data['hospital']}")
                except Exception as e:
                    print(f"⚠ Hospital field could not be filled: {str(e)}")

            # Fill Treatment field
            print("Filling in treatment field...")
            treatment_field = await page.query_selector(
                'input[name="treatment"], input[placeholder*="Treatment"], input[placeholder*="treatment"], '
                'input[name="specialty"], input[placeholder*="Specialty"]'
            )
            if treatment_field:
                await treatment_field.fill(search_data["treatment"])
                print(f"✓ Treatment filled: {search_data['treatment']}")
                time.sleep(1)
            else:
                print("⚠ Treatment field not found, trying alternative selectors...")
                try:
                    inputs = await page.query_selector_all('input[type="text"]')
                    if len(inputs) >= 3:
                        await inputs[2].fill(search_data["treatment"])
                        print(f"✓ Treatment filled using alternative method: {search_data['treatment']}")
                except Exception as e:
                    print(f"⚠ Treatment field could not be filled: {str(e)}")

            # Take screenshot before submission
            print("Taking screenshot of filled form...")
            await page.screenshot(path="hospital_search_filled.png")
            print("✓ Screenshot saved: hospital_search_filled.png")

            # Find and click search button
            print("Looking for search button...")
            search_button = await page.query_selector(
                'button:has-text("Search"), button:has-text("search"), '
                'button[type="submit"], input[type="submit"], '
                'button:has-text("Submit"), a:has-text("Search")'
            )

            if search_button:
                print("Clicking search button...")
                await search_button.click()

                # Wait for search results
                await page.wait_for_load_state("networkidle")
                time.sleep(2)

                # Take final screenshot
                await page.screenshot(path="hospital_search_results.png")
                print("✓ Search executed successfully!")
                print("✓ Screenshot saved: hospital_search_results.png")
            else:
                print("⚠ Search button not found")
                print("Form is filled but search was not executed. Here's what was filled:")
                print(f"  Location: {search_data['location']}")
                print(f"  Hospital: {search_data['hospital']}")
                print(f"  Treatment: {search_data['treatment']}")

        except Exception as e:
            print(f"❌ Error occurred: {str(e)}")
            await page.screenshot(path="hospital_search_error.png")
            print("Error screenshot saved: hospital_search_error.png")

        finally:
            # Close browser
            await browser.close()
            print("Browser closed.")
            page.wait_for_timeout(5000)


if __name__ == "__main__":
    print("Starting Hospital Network Search Automation...")
    print("=" * 50)
    asyncio.run(search_hospital_network())
    print("=" * 50)
    print("Script completed!")

