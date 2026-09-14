from __future__ import annotations

import allure
import pytest
import re
from playwright.sync_api import expect

from pages.product_listing_page import ProductListingPage


@pytest.mark.smoke
@pytest.mark.e2e
@allure.title("Products listing displays WooCommerce product cards")
@allure.description("Verify product cards contain names, prices, and an action.")
def test_products_listing(page) -> None:
    listing = ProductListingPage(page)
    with allure.step("Open products listing"):
        listing.open()
        expect(page).to_have_url(re.compile(r"/products/?"))
        page.wait_for_timeout(2000)
    with allure.step("Inspect product cards"):
        expect(listing.products().first).to_be_visible()
        card = listing.product()
        expect(card.locator("h2, h3, .woocommerce-loop-product__title").first).to_be_visible()
        expect(card.locator(".price, .amount").first).to_be_visible()
        expect(card.locator("a, button").last).to_be_visible()


@pytest.mark.regression
@allure.title("Whiteboards category lists relevant products")
@allure.description("Verify a representative product category page loads.")
def test_whiteboards_category(page) -> None:
    listing = ProductListingPage(page)
    listing.open("/product-category/whiteboards/")
    expect(page).to_have_url(re.compile(r"/product-category/whiteboards/?"))
    expect(listing.products().first).to_be_visible()
