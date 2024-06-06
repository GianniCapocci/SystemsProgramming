from pydantic import BaseModel, Field
from typing import Literal
from datetime import date


class User(BaseModel):
    user_id: str
    birth_year: int = Field(..., gt=1900, lt=2025)
    country: str
    currency: str
    gender: Literal['male', 'female']
    registration_date: date
