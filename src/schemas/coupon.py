from pydantic import BaseModel
from typing import List
from datetime import date


class Selection(BaseModel):
    event_id: str
    stake: float


class Coupon(BaseModel):
    coupon_id: str
    user_id: str
    stake: float
    timestamp: date
    selections: List[Selection]
