import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.config import get_settings


settings = get_settings()


@pytest.mark.ui
@pytest.mark.smoke
def test_standard_user_can_log_in(page: Page) -> None:
    login_page = LoginPage(page)
    products_page = ProductsPage(page)

    login_page.open()
    login_page.login(
        settings.standard_user,
        settings.standard_password,
    )

    expect(page).to_have_url(
        f"{settings.ui_base_url}/inventory.html"
    )
    expect(products_page.title).to_have_text("Products")

@pytest.mark.ui
@pytest.mark.regression
def test_invalid_password_displays_error(
    page: Page,
) -> None:
    login_page = LoginPage(page)

    login_page.open()
    login_page.login(
        settings.standard_user,
        "incorrect-password",
    )

    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_contain_text(
        "Username and password do not match"
    )

