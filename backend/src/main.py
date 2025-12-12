from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from sqlmodel import Session
try:
    # When run as a package (recommended)
    from . import database, models, crud
except Exception:
    # When run as a script (python main.py) — import from same folder
    import database, models, crud
from pydantic import BaseModel

app = FastAPI(title="Lonq Backend")

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PlaceOut(BaseModel):
    id: int
    external_id: str
    name: str
    lat: float
    long: float
    image: Optional[str]
    description: Optional[str]
    country: Optional[str]
    rating: Optional[float]
    distance: Optional[str]
    tags: List[str]


class TrackRequest(BaseModel):
    user_id: str
    action: Optional[str] = "visit"
    place_id: Optional[str] = None


@app.on_event("startup")
def on_startup():
    database.create_db_and_tables()


def get_session():
    yield from database.get_session()


@app.get("/places", response_model=List[PlaceOut])
def list_places(limit: Optional[int] = None, session: Session = Depends(get_session)):
    places = crud.get_places(session, limit)
    out = []
    for p in places:
        tags = []
        if p.tags:
            tags = [t for t in p.tags.split(",") if t]
        out.append(PlaceOut(
            id=p.id,
            external_id=p.external_id,
            name=p.name,
            lat=p.lat,
            long=p.long,
            image=p.image,
            description=p.description,
            country=p.country,
            rating=p.rating,
            distance=p.distance,
            tags=tags
        ))
    return out


@app.get("/places/{place_id}", response_model=PlaceOut)
def get_place(place_id: int, session: Session = Depends(get_session)):
    p = crud.get_place(session, place_id)
    if not p:
        raise HTTPException(status_code=404, detail="Place not found")
    tags = p.tags.split(",") if p.tags else []
    return PlaceOut(
        id=p.id,
        external_id=p.external_id,
        name=p.name,
        lat=p.lat,
        long=p.long,
        image=p.image,
        description=p.description,
        country=p.country,
        rating=p.rating,
        distance=p.distance,
        tags=[t for t in tags if t]
    )


@app.post("/users/track")
def track_user(req: TrackRequest, session: Session = Depends(get_session)):
    user = crud.create_user_action(session, req.user_id, req.action or "visit", req.place_id)
    return {"user_id": user.user_id, "visits": user.visits, "last_seen": str(user.last_seen)}
