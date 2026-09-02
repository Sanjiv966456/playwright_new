from .base_page import BasePage

class PropertiesPage(BasePage):
    LISTING_SELECTOR = ".listing, .property, .property-listing, .insta-item, .wp-block-cover"

    def goto_properties(self):
        return self.goto("/properties/")

    def has_listings(self) -> bool:
        return bool(self.page.query_selector(self.LISTING_SELECTOR))

    def first_listing_title(self):
        node = self.page.query_selector(self.LISTING_SELECTOR + " a, " + self.LISTING_SELECTOR)
        return node.inner_text().strip() if node else None

