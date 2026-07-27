import re

import pytest
from playwright.sync_api import Page, expect
from pytest_bdd import (
    given,
    parsers,
    scenarios,
    then,
    when,
)

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.config import get_settings

scenarios("../../features/checkout.feature")

settings = get_settings()


@pytest.fixture
def bdd_context() -> dict:
    return {}


@given("the customer is logged in")
def customer_is_logged_in(
    page: Page,
    bdd_context: dict,
) -> None:
    login_page = LoginPage(page)
    login_page.open()

    login_page.login(
        settings.standard_user,
        settings.standard_password,
    )

    expect(page).to_have_url(re.compile(r".*/inventory\.html$"))

    bdd_context["page"] = page


@when(parsers.parse('the customer adds "{product_name}" ' "to the cart"))
def add_product(
    page: Page,
    product_name: str,
) -> None:
    products_page = ProductsPage(page)

    products_page.add_product_to_cart(product_name)
    products_page.open_cart()

    cart_page = CartPage(page)

    expect(cart_page.product(product_name)).to_be_visible()


@when("the customer completes checkout")
def complete_checkout(page: Page) -> None:
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    cart_page.checkout()

    checkout_page.enter_customer_details(
        first_name="Thejesh",
        last_name="Krishnamurthy",
        postal_code="D01",
    )

    checkout_page.finish_order()


@then("an order confirmation should be displayed")
def verify_confirmation(page: Page) -> None:
    checkout_page = CheckoutPage(page)

    expect(checkout_page.confirmation_header).to_have_text("Thank you for your order!")
