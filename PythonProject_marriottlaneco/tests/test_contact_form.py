from pages.contact_page import ContactPage
import pytest


def test_contact_form_submit_smoke(page, base_url):
    contact = ContactPage(page, base_url=base_url)
    # Try to navigate to a contact page and submit a simple message
    try:
        contact.goto_contact()
    except Exception:
        # fallback: try to click an internal contact link
        page.goto(base_url)
        link = page.query_selector("a[href*='contact']")
        assert link, "No contact link found on site"
        link.click()
        page.wait_for_load_state('networkidle')
    # Attempt to submit
    ok = contact.submit_contact_form("Test User", "test@example.com", "This is a test message from Playwright.")
    # We don't expect a specific success response on all WP installs; assert that we attempted submit
    assert ok, "Contact form submit attempt failed (form not found or submission error)"

