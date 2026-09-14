from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):
    CATEGORY_LINKS = {
        "Whiteboards": "/product-category/whiteboards/",
        "Speciality Boards": "/product-category/speciality-boards/",
        "Pinboards": "/product-category/pinboards/",
        "Mobile Literacy Units": "/product-category/mobile-literacy-units/",
        "Sports & Recreation": "/product-category/sports-recreation/",
        "Partitions": "/product-category/partitions/",
    }

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> None:
        self.navigate("/")

    def logo(self):
        return self.first_visible("header img", "a.custom-logo-link img", "img[alt*='Whiteboard']")

    def shop_products(self):
        return self.first_visible("a:has-text('Shop Products')", "a[href*='/products']")

    def free_quote(self):
        return self.first_visible("a:has-text('Get a Free Quote')", "button:has-text('Free Quote')")

    def category(self, name: str):
        return self.first_visible(f"a:has-text('{name}')", f"[class*='category'] a:has-text('{name}')")

    def category_tile(self, name: str):
        return self.first_visible(
            f"text='{name}'",
            f"[class*='category']:has-text('{name}')",
            f"[class*='collection']:has-text('{name}')",
        )

    def featured_tab(self, name: str):
        return self.first_visible(
            f"button:has-text('{name}')",
            f"a:has-text('{name}')",
            f"li:has-text('{name}')",
            f"[class*='tab']:has-text('{name}')",
        )

    def footer(self):
        return self.page.locator("footer")
