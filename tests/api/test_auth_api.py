import pytest
from playwright.sync_api import APIRequestContext

from api_clients.auth_client import AuthClient
from utils.config import get_settings

settings = get_settings()


@pytest.mark.api
@pytest.mark.smoke
def test_valid_credentials_return_auth_token(
    api_context: APIRequestContext,
) -> None:
    auth_client = AuthClient(api_context)

    response = auth_client.create_token(
        username=settings.api_username,
        password=settings.api_password,
    )

    assert response.status == 200, (
        f"Expected status 200, but received {response.status}. "
        f"Response: {response.text()}"
    )

    response_body = response.json()

    assert "token" in response_body
    assert isinstance(response_body["token"], str)
    assert response_body["token"].strip() != ""


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.parametrize(
    ("username", "password"),
    [
        ("invalid-user", "password123"),
        ("admin", "invalid-password"),
        ("", ""),
    ],
)
def test_invalid_credentials_do_not_return_auth_token(
    api_context: APIRequestContext,
    username: str,
    password: str,
) -> None:
    auth_client = AuthClient(api_context)

    response = auth_client.create_token(
        username=username,
        password=password,
    )

    assert response.status == 200, (
        f"Expected Restful Booker to return status 200, "
        f"but received {response.status}. Response: {response.text()}"
    )

    response_body = response.json()

    assert "token" not in response_body
    assert "reason" in response_body
    assert response_body["reason"] == "Bad credentials"
