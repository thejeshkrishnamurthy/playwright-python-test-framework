import pytest
from playwright.sync_api import APIRequestContext

from api_clients.booking_client import BookingClient
from database.db_client import (
    get_booking,
    insert_booking,
)


@pytest.mark.integration
@pytest.mark.database
def test_api_booking_matches_database_record(
    api_context: APIRequestContext,
    valid_booking_payload: dict,
) -> None:
    client = BookingClient(api_context)

    response = client.create_booking(valid_booking_payload)

    assert response.status == 200

    response_body = response.json()
    booking_id = response_body["bookingid"]

    insert_booking(
        booking_id=booking_id,
        first_name=valid_booking_payload["firstname"],
        last_name=valid_booking_payload["lastname"],
        total_price=valid_booking_payload["totalprice"],
        status="CREATED",
    )

    database_record = get_booking(booking_id)

    assert database_record is not None
    assert database_record[0] == booking_id
    assert database_record[1] == valid_booking_payload["firstname"]
    assert database_record[3] == valid_booking_payload["totalprice"]
