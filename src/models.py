from pydantic import BaseModel
from datetime import date
from typing import Optional, Dict

class WeatherRequestCreate(BaseModel):
    user_name: str
    location_input: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class WeatherRequestUpdate(BaseModel):
    location_input: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class WeatherResponse(BaseModel):
    id: Optional[int] = None
    user_name: str
    location_input: str
    date_: Optional[date]
    type: str
    data: Dict[str, any]

    class Config:
        arbitrary_types_allowed = True