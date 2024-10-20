from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models, auth
from app.database import SessionLocal, get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.debug(f"Received user data: {user}")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
