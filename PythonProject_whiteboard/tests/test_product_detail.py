from __future__ import annotations

import allure
import pytest
from playwright.sync_api import expect

from pages.product_detail_page import ProductDetailPage


@pytest.mark.smoke
@pytest.mark.e2e
@allure.title("Product detail page shows purchase controls")
@allure.description("Verify title, price, image, options, description, and add-to-cart control.")
def test_product_detail(page) -> None:
    product = ProductDetailPage(page)
    with allure.step("Open representative product"):
        product.open()
    with allure.step("Verify product information"):
        expect(product.title()).to_be_visible()
        expect(product.price()).to_be_visible()
        expect(page.locator(".woocommerce-product-gallery img, .product img").first).to_be_visible()
        expect(page.locator(".woocommerce-Tabs-panel, .product-description, .description").first).to_be_visible()
    with allure.step("Verify options and add-to-cart"):
        product.select_first_option()
        expect(page.locator("button.single_add_to_cart_button, button:has-text('Add to cart')").first).to_be_visible()
