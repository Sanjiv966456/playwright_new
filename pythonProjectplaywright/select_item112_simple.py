from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://testautomationpractice.blogspot.com/p/playwrightpractice.html", wait_until="domcontentloaded")

    # Long wait for content to dynamically load
    time.sleep(5)
    page.wait_for_timeout(2000)

    # Check page source for Item 112
    content = page.content()
    if "Item 112" in content:
        print("✓ 'Item 112' found in page content")
    else:
        print("❌ 'Item 112' NOT found in page content")

    # Try to find visible text "Item 112"
    try:
        item_112 = page.locator("text=Item 112")
        count = item_112.count()
        print(f"✓ Found {count} element(s) with 'Item 112' text")

        if count > 0:
            # Click on it
            item_112.nth(0).click()
            print("✓ Clicked Item 112!")
            page.screenshot(path="item112_selected.png")
            print("✓ Screenshot saved: item112_selected.png")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Alternative: find by role
    try:
        print("\n--- Looking for combobox/select elements ---")
        combobox = page.locator("[role='combobox'], [role='listbox']")
        print(f"✓ Found {combobox.count()} combobox/listbox elements")

        # Try getting all divs that might contain Item 112
        all_divs_with_item = page.locator("div:has-text('Item')")
        print(f"✓ Found {all_divs_with_item.count()} divs with 'Item' text")
    except Exception as e:
        print(f"Error: {e}")

    page.screenshot(path="page_final.png")
    print(f"\n✓ Final screenshot saved: page_final.png")

    page.wait_for_timeout(2000)
    browser.close()

