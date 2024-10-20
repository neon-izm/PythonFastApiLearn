from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/", response_model=list[schemas.Todo])
def read_todos(current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_todos(db, user_id=current_user.id)

@router.post("/", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo, user_id=current_user.id)
