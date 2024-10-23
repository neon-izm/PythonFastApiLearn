from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, auth
from app.database import get_db

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/", response_model=list[schemas.Todo])
def read_todos(
    current_user: schemas.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    todos = crud.get_todos(db, user_id=current_user.id)
    if todos is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos

@router.post("/", response_model=schemas.Todo)
def create_todo(
    todo: schemas.TodoCreate,
    current_user: schemas.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    return crud.create_todo(db=db, todo=todo, user_id=current_user.id)
