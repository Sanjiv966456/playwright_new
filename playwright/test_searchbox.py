import pytest
from playwright.sync_api import sync_playwright, Page

def test_hospital_search():
    with sync_playwright() as p:
        context = p.chromium.launch(headless=False, slow_mo=800).new_context(
            permissions=["geolocation"],
            geolocation={"latitude": 22.3072, "longitude": 73.1812}
        )
        page = context.new_page()
        page.goto("https://rules.nivabupa.com/hospital-network/", wait_until="networkidle")

        # --- Location: "City Name" placeholder ---
        page.get_by_placeholder("City Name").click()
        page.get_by_placeholder("City Name").fill("Vadodara")
        page.wait_for_timeout(1000)
        page.get_by_text("Vadodara").first.click()

        # --- Hospital: "Hospital Name" placeholder ---
        hospital_input = page.get_by_placeholder("Hospital Name")
        hospital_input.click()
        hospital_input.fill("Tapan Eye Care")
        page.wait_for_timeout(1000)
        # Try to select suggestion by keypress (more resilient than exact text match)
        try:
            hospital_input.press("ArrowDown")
            hospital_input.press("Enter")
        except Exception:
            # Fallback: click first suggestion if present
            try:
                page.get_by_role("option").first.click()
            except Exception:
                pass

        # --- Treatment: "Diagnosis/Treatment" placeholder ---
        treatment_input = page.get_by_placeholder("Diagnosis/Treatment")
        treatment_input.click()
        treatment_input.fill("Eye")
        page.wait_for_timeout(1000)
        # Select first suggestion via keypress
        try:
            treatment_input.press("ArrowDown")
            treatment_input.press("Enter")
        except Exception:
            try:
                page.get_by_role("option").first.click()
            except Exception:
                pass

        # --- Click Search button ---
        page.get_by_role("button", name="Search").click()
        page.wait_for_timeout(3000)
