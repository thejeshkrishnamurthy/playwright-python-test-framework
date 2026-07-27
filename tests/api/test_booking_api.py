import pytest
from jsonschema import validate
from playwright.sync_api import APIRequestContext

from api_clients.booking_client import BookingClient
from schemas.booking_schema import (
    BOOKING_RESPONSE_SCHEMA,
)


@pytest.mark.api
@pytest.mark.smoke
def test_create_and_retrieve_booking(
    api_context: APIRequestContext,
    valid_booking_payload: dict,
) -> None:
    client = BookingClient(api_context)

    create_response = client.create_booking(valid_booking_payload)

    assert create_response.status == 200

    created_booking = create_response.json()

    validate(
        instance=created_booking,
        schema=BOOKING_RESPONSE_SCHEMA,
    )

    booking_id = created_booking["bookingid"]

    retrieve_response = client.get_booking(booking_id)

    assert retrieve_response.status == 200

    retrieved_booking = retrieve_response.json()

    assert retrieved_booking["firstname"] == valid_booking_payload["firstname"]
    assert retrieved_booking["lastname"] == valid_booking_payload["lastname"]


@pytest.mark.api
@pytest.mark.regression
def test_booking_crud_lifecycle(
    api_context: APIRequestContext,
    api_token: str,
    valid_booking_payload: dict,
) -> None:
    client = BookingClient(api_context)

    create_response = client.create_booking(valid_booking_payload)
    assert create_response.status == 200

    booking_id = create_response.json()["bookingid"]

    updated_payload = {
        **valid_booking_payload,
        "firstname": "Updated",
        "totalprice": 300,
    }

    update_response = client.update_booking(
        booking_id,
        api_token,
        updated_payload,
    )

    assert update_response.status == 200
    assert update_response.json()["firstname"] == "Updated"

    patch_response = client.partially_update_booking(
        booking_id,
        api_token,
        {
            "additionalneeds": "Late checkout",
        },
    )

    assert patch_response.status == 200
    assert patch_response.json()["additionalneeds"] == "Late checkout"

    delete_response = client.delete_booking(
        booking_id,
        api_token,
    )

    assert delete_response.status in {
        200,
        201,
        204,
    }

    retrieve_response = client.get_booking(booking_id)

    assert retrieve_response.status == 404


@pytest.mark.api
@pytest.mark.regression
def test_update_booking_with_invalid_token_is_rejected(
    api_context: APIRequestContext,
    valid_booking_payload: dict,
) -> None:
    client = BookingClient(api_context)

    create_response = client.create_booking(valid_booking_payload)
    booking_id = create_response.json()["bookingid"]

    update_response = client.update_booking(
        booking_id,
        "invalid-token",
        valid_booking_payload,
    )

    assert update_response.status in {
        401,
        403,
    }
