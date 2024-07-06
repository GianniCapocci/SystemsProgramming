user_schema = {
    "type": "object",
    "properties": {
        "user_id": {
            "type": "string"
        },
        "birth_year": {
            "type": "integer"
        },
        "country": {
            "type": "string"
        },
        "currency": {
            "type": "string"
        },
        "gender": {
            "type": "string"
        },
        "registration_date": {
            "type": "string",
            "format": "date"
        }
    },
    "required": ["user_id", "birth_year", "country", "currency", "gender", "registration_date"]
}
