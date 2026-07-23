import pytest
from playwright.sync_api import Page, expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.config import get_settings


settings = get_settings()


@pytest.mark.ui
@pytest.mark.smoke
def test_customer_can_complete_checkout(
    page: Page,
) -> None:
    login_page = LoginPage(page)
    products_page = ProductsPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    login_page.open()
    login_page.login(
        settings.standard_user,
        settings.standard_password,
    )

    products_page.add_product_to_cart(
        "Sauce Labs Backpack"
    )
    products_page.open_cart()

    expect(
        cart_page.product("Sauce Labs Backpack")
    ).to_be_visible()

    cart_page.checkout()

    checkout_page.enter_customer_details(
        first_name="Thejesh",
        last_name="Krishnamurthy",
        postal_code="D01",
    )

    checkout_page.finish_order()

    expect(
        checkout_page.confirmation_header
    ).to_have_text(
        "Thank you for your order!"
    )