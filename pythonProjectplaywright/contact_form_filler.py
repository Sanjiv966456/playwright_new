"""
Contact Form Automation Script
Fills the contact form at https://marriottlaneco.wpenginepowered.com/contact/
with valid test data using Playwright
"""

import asyncio
from playwright.async_api import async_playwright
import time


async def fill_contact_form():
    """Fill the contact form with valid data"""

    # Valid test data
    contact_data = {
        "name": "John Smith",
        "email": "john.smith@example.com",
        "phone": "+1-555-123-4567",
        "subject": "Inquiry About Services",
        "message": "Hello, I am interested in learning more about your services. Please contact me at your earliest convenience. Thank you!"
    }

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)  # Set to True for headless mode
        page = await browser.new_page()

        try:
            # Navigate to contact page
            print("Navigating to contact page...")
            await page.goto("https://marriottlaneco.wpenginepowered.com/contact/",
                          wait_until="networkidle")

            # Wait for page to load completely
            await page.wait_for_load_state("domcontentloaded")
            time.sleep(2)

            print("Page loaded successfully!")

            # Fill Name field
            print("Filling in name field...")
            name_field = await page.query_selector('input[name="name"], [placeholder*="Name"], [placeholder*="name"]')
            if name_field:
                await name_field.fill(contact_data["name"])
                print(f"✓ Name filled: {contact_data['name']}")
            else:
                print("⚠ Name field not found, trying alternative selectors...")
                await page.fill('input[type="text"]:first-of-type', contact_data["name"])

            # Fill Email field
            print("Filling in email field...")
            email_field = await page.query_selector('input[name="email"], input[type="email"], [placeholder*="Email"]')
            if email_field:
                await email_field.fill(contact_data["email"])
                print(f"✓ Email filled: {contact_data['email']}")
            else:
                print("⚠ Email field not found")

            # Fill Phone field
            print("Filling in phone field...")
            phone_field = await page.query_selector('input[name="phone"], input[name="telephone"], [placeholder*="Phone"]')
            if phone_field:
                await phone_field.fill(contact_data["phone"])
                print(f"✓ Phone filled: {contact_data['phone']}")
            else:
                print("⚠ Phone field not found")

            # Fill Subject/Title field if exists
            print("Filling in subject field...")
            subject_field = await page.query_selector('input[name="subject"], input[name="title"], [placeholder*="Subject"]')
            if subject_field:
                await subject_field.fill(contact_data["subject"])
                print(f"✓ Subject filled: {contact_data['subject']}")
            else:
                print("⚠ Subject field not found")

            # Fill Message/Message field
            print("Filling in message field...")
            message_field = await page.query_selector('textarea[name="message"], textarea, [placeholder*="Message"]')
            if message_field:
                await message_field.fill(contact_data["message"])
                print(f"✓ Message filled: {contact_data['message'][:50]}...")
            else:
                print("⚠ Message field not found")

            # Take screenshot before submission
            print("Taking screenshot of filled form...")
            await page.screenshot(path="contact_form_filled.png")
            print("✓ Screenshot saved: contact_form_filled.png")

            # Find and click submit button
            print("Looking for submit button...")
            submit_button = await page.query_selector(
                'button:has-text("Submit"), button:has-text("Send"), '
                'button[type="submit"], input[type="submit"]'
            )

            if submit_button:
                print("Submitting form...")
                await submit_button.click()

                # Wait for submission confirmation
                await page.wait_for_load_state("networkidle")
                time.sleep(2)

                # Take final screenshot
                await page.screenshot(path="contact_form_submitted.png")
                print("✓ Form submitted successfully!")
                print("✓ Screenshot saved: contact_form_submitted.png")
            else:
                print("⚠ Submit button not found")
                print("Form is filled but not submitted. Here's what was filled:")
                print(f"  Name: {contact_data['name']}")
                print(f"  Email: {contact_data['email']}")
                print(f"  Phone: {contact_data['phone']}")
                print(f"  Subject: {contact_data['subject']}")
                print(f"  Message: {contact_data['message']}")

        except Exception as e:
            print(f"❌ Error occurred: {str(e)}")
            await page.screenshot(path="error_screenshot.png")
            print("Error screenshot saved: error_screenshot.png")

        finally:
            # Close browser
            await browser.close()
            print("Browser closed.")


if __name__ == "__main__":
    print("Starting Contact Form Automation...")
    print("=" * 50)
    asyncio.run(fill_contact_form())
    print("=" * 50)
    print("Script completed!")

