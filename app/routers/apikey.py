from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.crud.apikey import create_api_key, delete_api_key
from app.dependencies.auth import get_current_user
from app.models.user import User
import uuid
from typing import Optional
from sqlmodel import select
from app.models.apikey import APIKey

router = APIRouter()

@router.post("/apikeys")
def create_user_api_key(current_user: User = Depends(get_current_user),
                         name: str = None, 
                         user_project_id: uuid.UUID = None,
                         session: Session = Depends(get_session)):
    return create_api_key(session, current_user.id, name, user_project_id)

@router.delete("/apikeys/{key_id}")
def remove_user_api_key(key_id: uuid.UUID, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    api_key = delete_api_key(session, key_id)
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    return {"detail": "API key deleted"}

@router.get("/apikeys")
def get_user_api_keys(current_user: User = Depends(get_current_user), session: Session = Depends(get_session), user_project_id: Optional[uuid.UUID] = None):
    if user_project_id:
        api_keys = session.exec(select(APIKey).where(APIKey.user_project_id == user_project_id)).all()
    else:
        api_keys = []
        for project in current_user.projects:
            api_keys.extend(project.api_keys)
    return api_keys