from playwright.sync_api import Page, expect
import time

def test_drag_and_drop(page: Page):
    """Test to drag an element and drop it on target"""

    # Navigate to the test website
    page.goto("https://testautomationpractice.blogspot.com/?m=1")
    page.wait_for_timeout(3000)
    source = page.locator("#draggable")
    target = page.locator("#droppable")
    source.drag_to(target)



