from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from sqlmodel import Session, select

from app.database import get_session
from app.models.apikey import APIKey
from app.models.user import User, UserProject

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header), session: Session = Depends(get_session)):
    if api_key_header is None:
        raise HTTPException(
            status_code=403, detail="API key is required"
        )
    api_key = session.exec(select(APIKey).where(APIKey.key == api_key_header)).first()
    print("API KEY", api_key)
    if api_key is None:
        raise HTTPException(
            status_code=403, detail="Invalid API key"
        )
    user_project = session.exec(select(UserProject).where(UserProject.id == api_key.user_project_id)).first()
    print("User project", user_project)
    if user_project is None:
        raise HTTPException(
            status_code=403, detail="User project not found"
        )
    user = session.exec(select(User).where(User.id == user_project.user_id)).first()
    print("User", user)
    return user_project
