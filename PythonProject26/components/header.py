"""Header component locators and actions."""

from playwright.sync_api import Locator, Page


class Header:
    """Semantic accessors for the site header."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.root = page.get_by_role("banner")

    @property
    def links(self) -> Locator:
        """All links inside the site header."""
        return self.root.get_by_role("link")

    @property
    def logo(self) -> Locator:
        """A home link containing the site's logo image."""
        return self.root.get_by_role("link").filter(has=self.page.locator("img")).first

    @property
    def menu_button(self) -> Locator:
        """Mobile navigation toggle, if one exists."""
        return self.root.get_by_role("button", name="Menu", exact=False).or_(
            self.root.get_by_role("button", name="Navigation", exact=False)
        ).first
