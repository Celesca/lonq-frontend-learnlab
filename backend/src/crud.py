from typing import List, Optional
from sqlmodel import Session, select
try:
    from . import models
except Exception:
    import models

def get_places(session: Session, limit: Optional[int] = None) -> List[models.Place]:
    stmt = select(models.Place).order_by(models.Place.id)
    if limit:
        stmt = stmt.limit(limit)
    return session.exec(stmt).all()

def get_place(session: Session, place_id: int) -> Optional[models.Place]:
    return session.get(models.Place, place_id)

def find_place_by_external_id(session: Session, external_id: str) -> Optional[models.Place]:
    stmt = select(models.Place).where(models.Place.external_id == external_id)
    return session.exec(stmt).first()

def create_user_action(session: Session, user_id: str, action: str, place_id: Optional[str] = None):
    ua = models.UserAction(user_id=user_id, action=action, place_id=place_id)
    session.add(ua)
    session.commit()
    session.refresh(ua)

    # update/create user summary
    user = session.exec(select(models.User).where(models.User.user_id == user_id)).first()
    from datetime import datetime
    if not user:
        user = models.User(user_id=user_id, visits=1, last_seen=datetime.utcnow(), last_action=action, last_place=place_id)
        session.add(user)
    else:
        user.visits = (user.visits or 0) + 1
        user.last_seen = datetime.utcnow()
        user.last_action = action
        user.last_place = place_id
    session.commit()
    return user
