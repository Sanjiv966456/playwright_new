from playwright.sync_api import Page, expect

def test_newpage(page: Page):
    context = page.context
    
    # Start tracing with correct API
    context.tracing.start(snapshots=True, screenshots=True, sources=True)
    
    page.goto("https://fixergroupdev.wpenginepowered.com/")
    page.get_by_role("banner").get_by_role("link", name="Partner with Fixer Group").click()
    page.wait_for_timeout(5000)

    page.locator("#enquire-fast").get_by_role("button", name="Submit Now").click()
    page.wait_for_timeout(5000)
    page.screenshot(path="enquire_now.png", full_page=True)
    page.context.storage_state(path="state.json")
    
    # Stop tracing and save to file
    context.tracing.stop(path="trace.zip")