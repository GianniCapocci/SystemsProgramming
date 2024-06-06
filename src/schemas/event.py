from typing import List
from pydantic import BaseModel
from datetime import date


class Event(BaseModel):
    begin_timestamp: date
    country: str
    end_timestamp: date
    event_id: str
    league: str
    participants: List[str]
    sport: str
