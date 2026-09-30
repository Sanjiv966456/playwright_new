from playwright.sync_api import Page,expect

def test_select_multiple_colors(page: Page):
    page.goto("https://testautomationpractice.blogspot.com/")
    page.wait_for_timeout(5000)

    # Select multiple colors
    colors_to_select = ["Red", "Green", "Blue"]
    for color in colors_to_select:
        page.get_by_label("Colors:", exact=True).select_option(color)
    page.wait_for_timeout(2000)

    # Take a screenshot after selecting colors
    page.screenshot(path="multiple_colors_selected.png", full_page=True)