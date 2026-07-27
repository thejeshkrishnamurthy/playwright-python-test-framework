BOOKING_RESPONSE_SCHEMA = {
    "type": "object",
    "required": [
        "bookingid",
        "booking",
    ],
    "properties": {
        "bookingid": {
            "type": "integer",
        },
        "booking": {
            "type": "object",
            "required": [
                "firstname",
                "lastname",
                "totalprice",
                "depositpaid",
                "bookingdates",
            ],
            "properties": {
                "firstname": {
                    "type": "string",
                },
                "lastname": {
                    "type": "string",
                },
                "totalprice": {
                    "type": "integer",
                },
                "depositpaid": {
                    "type": "boolean",
                },
                "bookingdates": {
                    "type": "object",
                    "required": [
                        "checkin",
                        "checkout",
                    ],
                },
            },
        },
    },
}
