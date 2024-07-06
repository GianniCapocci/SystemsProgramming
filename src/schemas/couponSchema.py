coupon_schema = {
    "type": "object",
    "properties": {
        "coupon_id": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50
        },
        "user_id": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50
        },
        "stake": {
            "type": "number"
        },
        "timestamp": {
            "type": "string",
            "format": "date-time"
        },
        "selections": {
            "type": "array",
            "items": {"type": "object"}
        }
    },
    "required": ["coupon_id", "user_id", "stake", "timestamp", "selections"]
}
