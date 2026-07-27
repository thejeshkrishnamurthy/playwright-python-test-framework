import pytest
from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Page

from pages.login_page import LoginPage


@pytest.mark.accessibility
def test_login_page_has_no_critical_violations(
    page: Page,
) -> None:
    login_page = LoginPage(page)
    login_page.open()

    results = Axe().run(page)

    critical_violations = [
        violation
        for violation in results.response["violations"]
        if violation.get("impact") == "critical"
    ]

    assert critical_violations == []
