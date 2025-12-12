import json
import os
from sqlmodel import Session
try:
    from .database import engine, create_db_and_tables
    from .models import Place
except Exception:
    from database import engine, create_db_and_tables
    from models import Place

THIS_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
JSON_FILE = os.path.join(DATA_DIR, "travel_places.json")


def load_json():
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def seed():
    create_db_and_tables()
    data = load_json()
    with Session(engine) as session:
        existing = session.exec("SELECT COUNT(*) FROM place").one()
        # If already seeded, skip inserting duplicates
        if existing and existing[0] > 0:
            print("DB already seeded")
            return

        for item in data:
            tags = item.get("tags")
            tags_str = ",".join(tags) if isinstance(tags, list) else (tags or "")
            p = Place(
                external_id=item.get("id"),
                name=item.get("name"),
                lat=item.get("lat") or 0.0,
                long=item.get("long") or 0.0,
                image=item.get("image"),
                description=item.get("description"),
                country=item.get("country"),
                rating=item.get("rating"),
                distance=item.get("distance"),
                tags=tags_str,
            )
            session.add(p)
        session.commit()
        print("Seeded places into DB")


if __name__ == "__main__":
    seed()
