from datetime import date

from pydantic import BaseModel, Field


class BookingDates(BaseModel):
    checkin: date
    checkout: date


class BookingRequest(BaseModel):
    firstname: str = Field(
        min_length=1,
        max_length=100,
    )
    lastname: str = Field(
        min_length=1,
        max_length=100,
    )
    totalprice: int = Field(gt=0)
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: str | None = None
