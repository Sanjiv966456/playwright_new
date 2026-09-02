from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    page = p.chromium.launch(headless=False).new_page()
    page.goto("https://testautomationpractice.blogspot.com/p/playwrightpractice.html")
    page.locator("select").scroll_into_view_if_needed()
    page.locator("select").select_option(label="Item 112")

