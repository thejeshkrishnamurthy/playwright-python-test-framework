from playwright.sync_api import APIRequestContext, APIResponse

from api_clients.base_api_client import BaseApiClient


class BookingClient(BaseApiClient):
    def __init__(
        self,
        api_context: APIRequestContext,
    ) -> None:
        super().__init__(api_context)

    def create_booking(
        self,
        payload: dict[str, object],
    ) -> APIResponse:
        return self.post(
            "/booking",
            data=payload,
        )

    def get_booking(
        self,
        booking_id: int,
    ) -> APIResponse:
        return self.get(f"/booking/{booking_id}")

    def update_booking(
        self,
        booking_id: int,
        token: str,
        payload: dict[str, object],
    ) -> APIResponse:
        return self.put(
            f"/booking/{booking_id}",
            headers={
                "Cookie": f"token={token}",
            },
            data=payload,
        )

    def partially_update_booking(
        self,
        booking_id: int,
        token: str,
        payload: dict[str, object],
    ) -> APIResponse:
        return self.patch(
            f"/booking/{booking_id}",
            headers={
                "Cookie": f"token={token}",
            },
            data=payload,
        )

    def delete_booking(
        self,
        booking_id: int,
        token: str,
    ) -> APIResponse:
        return self.delete(
            f"/booking/{booking_id}",
            headers={
                "Cookie": f"token={token}",
            },
        )
