event_schema = {
    "type": "object",
    "properties": {
        "event_id": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50
        },
        "begin_timestamp": {
            "type": "string",
            "format": "date-time"
        },
        "end_timestamp": {
            "type": "string",
            "format": "date-time"
        },
        "country": {
            "type": "string",
            "minLength": 1,
            "maxLength": 100
        },
        "league": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50
        },
        "participants": {
            "type": "array",
            "items": {"type": "string"}
        },
        "sport": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50
        }
    },
    "required": ["event_id", "begin_timestamp", "end_timestamp", "country", "league", "participants", "sport"]
}
