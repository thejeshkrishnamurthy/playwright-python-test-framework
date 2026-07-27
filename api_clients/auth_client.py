from playwright.sync_api import APIRequestContext, APIResponse

from api_clients.base_api_client import BaseApiClient


class AuthClient(BaseApiClient):
    def __init__(
        self,
        api_context: APIRequestContext,
    ) -> None:
        super().__init__(api_context)

    def create_token(
        self,
        username: str,
        password: str,
    ) -> APIResponse:
        return self.post(
            "/auth",
            data={
                "username": username,
                "password": password,
            },
        )
