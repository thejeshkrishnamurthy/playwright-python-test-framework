from collections.abc import Generator

import pytest
from playwright.sync_api import APIRequestContext, Playwright

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
) -> Generator[APIRequestContext, None, None]:
    context = playwright.request.new_context(
        base_url=settings.api_base_url,
        extra_http_headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )

    yield context

    context.dispose()