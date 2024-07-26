from sqlmodel import Session
from app.models.apikey import APIKey
from uuid import uuid4
from fastapi import HTTPException
import uuid

def create_api_key(db: Session, user_id: uuid.UUID, name: str = None, user_project_id: uuid.UUID = None):
    # Check if the project has reached the maximum number of API keys
    existing_keys = db.query(APIKey).filter(APIKey.user_project_id == user_project_id).count()
    if existing_keys >= 3:
        raise HTTPException(status_code=400, detail="Maximum number of API keys for this project reached")
    
    api_key = APIKey(key=str(uuid4()), user_id=user_id, name=name, user_project_id=user_project_id)
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return api_key

def delete_api_key(db: Session, key_id: uuid.UUID):
    api_key = db.get(APIKey, key_id)
    if api_key:
        db.delete(api_key)
        db.commit()
    return api_key
