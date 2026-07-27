# tests/ui/test_multiple_users.py

import re

import pytest
from playwright.sync_api import Browser, expect

from pages.login_page import LoginPage
from utils.config import get_settings

settings = get_settings()


@pytest.mark.ui
@pytest.mark.regression
def test_two_users_have_isolated_sessions(
    browser: Browser,
) -> None:
    user_one_context = browser.new_context(
        base_url=settings.ui_base_url,
    )
    user_two_context = browser.new_context(
        base_url=settings.ui_base_url,
    )

    user_one_page = user_one_context.new_page()
    user_two_page = user_two_context.new_page()

    try:
        first_login = LoginPage(user_one_page)
        second_login = LoginPage(user_two_page)

        first_login.open()
        first_login.login(
            settings.standard_user,
            settings.standard_password,
        )

        second_login.open()
        second_login.login(
            "problem_user",
            settings.standard_password,
        )

        expect(user_one_page).to_have_url(re.compile(r".*/inventory\.html$"))
        expect(user_two_page).to_have_url(re.compile(r".*/inventory\.html$"))

        assert user_one_page.context != user_two_page.context

    finally:
        user_one_context.close()
        user_two_context.close()
