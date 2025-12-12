from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Place(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    external_id: str = Field(index=True)
    name: str
    lat: float
    long: float
    image: Optional[str]
    description: Optional[str]
    country: Optional[str]
    rating: Optional[float]
    distance: Optional[str]
    tags: Optional[str]  # comma separated

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, unique=True)
    visits: int = 0
    last_seen: Optional[datetime] = None
    last_action: Optional[str] = None
    last_place: Optional[str] = None

class UserAction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    action: str
    place_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
