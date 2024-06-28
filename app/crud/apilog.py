from sqlmodel import Session
from app.models.apilog import APILog
from app.schemas.apilog import APILogCreate
from app.crud.user import increment_request_count, User

def create_apilog(db: Session, user_id: int, apilog: APILogCreate):
    user = db.get(User, user_id)
    increment_request_count(user, db)
    db_apilog = APILog(user_id=user_id, **apilog.dict())
    db.add(db_apilog)
    db.commit()
    db.refresh(db_apilog)
    return db_apilog
