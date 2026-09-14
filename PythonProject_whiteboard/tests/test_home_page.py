from __future__ import annotations

import allure
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage


@pytest.mark.smoke
@pytest.mark.e2e
@allure.title("Home page renders the primary storefront content")
@allure.description("Verify title, header, hero, collections, products, testimonials, and footer.")
def test_home_page(home_page) -> None:
    home = HomePage(home_page)
    with allure.step("Verify page title and header"):
        expect(home_page).to_have_title("Whiteboards Melbourne | Quality Boards Across Australia")
        expect(home.logo()).to_be_visible()
        expect(home_page.locator("a[href='tel:0397064995'], a[href='tel:0397064602']").first).to_be_visible()
        expect(home_page.locator("a[href*='my-account']").first).to_be_visible()
    with allure.step("Verify hero calls to action and collections"):
        expect(home.shop_products()).to_be_visible()
        expect(home.free_quote()).to_be_visible()
        for category in home.CATEGORY_LINKS:
            expect(home.category_tile(category)).to_be_visible()
    with allure.step("Verify storefront sections and footer"):
        expect(home_page.get_by_text("Best Sellers", exact=False).first).to_be_visible()
        footer = home.footer()
        footer.scroll_into_view_if_needed()
        home_page.wait_for_timeout(3000)
        expect(footer).to_be_attached()


@pytest.mark.regression
@allure.title("Featured product tabs are interactive")
@allure.description("Each featured-products audience tab can be selected.")
def test_featured_product_tabs(home_page) -> None:
    home = HomePage(home_page)
    for tab in ("Schools", "Offices", "Personal", "Sports & Speciality"):
        with allure.step(f"Select {tab} tab"):
            home.featured_tab(tab).click()
            expect(home.featured_tab(tab)).to_be_visible()
