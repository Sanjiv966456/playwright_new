from playwright.sync_api import sync_playwright

def enter_dates():
    """Simple script to enter dates in all date pickers"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            # Navigate to the website
            page.goto("https://testautomationpractice.blogspot.com/?m=1")
            page.wait_for_timeout(3000)
            
            # Date Picker 1 (mm/dd/yyyy format text input)
            print("Entering Date Picker 1...")
            dp1 = page.locator('input[type="text"]').nth(0)
            dp1.clear()
            dp1.type("12/15/2024")
            print("[OK] Date Picker 1: 12/15/2024")
            page.wait_for_timeout(1000)
            
            # Date Picker 2 (dd/mm/yyyy format text input)
            print("Entering Date Picker 2...")
            dp2 = page.locator('input[type="text"]').nth(1)
            dp2.clear()
            dp2.type("20/06/2025")
            print("[OK] Date Picker 2: 20/06/2025")
            page.wait_for_timeout(1000)
            
            # Date Picker 3 - Start Date (HTML5 date input needs YYYY-MM-DD)
            print("Entering Start Date...")
            start_date = page.locator('#start-date')
            start_date.fill("2023-10-01")
            print("[OK] Start Date: 2023-10-01")
            page.wait_for_timeout(1000)
            
            # Date Picker 3 - End Date
            print("Entering End Date...")
            end_date = page.locator('#end-date')
            end_date.fill("2024-12-31")
            print("[OK] End Date: 2024-12-31")
            page.wait_for_timeout(2000)
            
            # Take screenshot
            page.screenshot(path="dates_entered.png", full_page=True)
            print("[OK] Screenshot saved: dates_entered.png")
            
            page.wait_for_timeout(2000)
            
        except Exception as e:
            print(f"[ERROR] {str(e)}")
        finally:
            browser.close()

if __name__ == "__main__":
    enter_dates()
