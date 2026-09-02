from playwright.sync_api import sync_playwright

# Minimal 3-line script: launch headed browser, open page, screenshot logo (fallback selectors)
with sync_playwright() as p:
    page = p.chromium.launch(headless=False).new_page(); page.goto("https://marriottlaneco.wpenginepowered.com/")
    page.wait_for_load_state("networkidle")
    page.locator('img[alt*="Marriott"], img[src*="logo"], header img, img.logo').first.screenshot(path="marriott_logo.png")


