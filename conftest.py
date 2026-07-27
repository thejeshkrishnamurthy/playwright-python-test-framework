from collections.abc import Generator

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from api_clients.auth_client import AuthClient
from utils.config import get_settings

settings = get_settings()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "base_url": settings.ui_base_url,
        "viewport": {
            "width": 1440,
            "height": 900,
        },
        "ignore_https_errors": False,
    }


@pytest.fixture(scope="session")
def api_context(
    playwright: Playwright,
) -> Generator[APIRequestContext]:
    context = playwright.request.new_context(
        base_url=settings.api_base_url,
        extra_http_headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    yield context

    context.dispose()


@pytest.fixture(scope="session")
def api_token(api_context: APIRequestContext) -> str:
    auth_client = AuthClient(api_context)

    response = auth_client.create_token(
        settings.api_username,
        settings.api_password,
    )

    assert response.status == 200

    response_body = response.json()

    assert "token" in response_body

    return response_body["token"]


@pytest.fixture
def valid_booking_payload() -> dict:
    return {
        "firstname": "Thejesh",
        "lastname": "Krishnamurthy",
        "totalprice": 250,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-08-01",
            "checkout": "2026-08-05",
        },
        "additionalneeds": "Breakfast",
    }
