from .base_page import BasePage

class HomePage(BasePage):
    HERO_SELECTOR = "header, .site-header, .hero, .page-hero"
    NAV_SELECTOR = "nav, .main-navigation, .site-navigation"
    FOOTER_SELECTOR = "footer, .site-footer"

    def goto_home(self):
        return self.goto("")

    def has_hero(self) -> bool:
        return bool(self.page.query_selector(self.HERO_SELECTOR))

    def has_nav(self) -> bool:
        return bool(self.page.query_selector(self.NAV_SELECTOR))

    def has_footer(self) -> bool:
        return bool(self.page.query_selector(self.FOOTER_SELECTOR))

    def find_link_by_partial(self, partial: str):
        return self.page.query_selector(f"a[href*='{partial}']")

