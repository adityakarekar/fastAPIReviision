from typing import Annotated
from fastapi import Depends,APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
router=APIRouter()
from models import Todos
from .auth import get_current_user


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]


class TodoRequest(BaseModel):
    title:str=Field(min_length=3)
    description:str=Field(min_length=3,max_length=100)
    priority:int=Field(gt=0,lt=6)
    complete:bool


@router.get("/",status_code=status.HTTP_200_OK)
def read_all(user:user_dependency,db:db_dependency):
    return db.query(Todos).filter(Todos.owner_id==user.get("id")[0]).all()


@router.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
def read_todo(user:user_dependency,db:db_dependency,todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get("id")[0]).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404,detail="Todo Item not found")

@router.post("/todo",status_code=status.HTTP_201_CREATED)
def create_todo(user:user_dependency,db:db_dependency,todo_request:TodoRequest):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    
    # print(f"user.get(id)={user.get("id")[0]} and type: {type(user.get("id")[0])}")
    todo_model=Todos(**todo_request.model_dump(),owner_id=user.get("id")[0])

    db.add(todo_model) # adds the data into the db
    db.commit() # does the actual operation /transaction of flushing the data into the db


@router.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
def update_todo(user:user_dependency,db:db_dependency,todo_request:TodoRequest,todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get("id")[0]).first()
    if todo_model is  None:
        raise HTTPException(status_code=404,detail="Item not found")
    todo_model.title=todo_request.title
    todo_model.description=todo_request.description
    todo_model.priority=todo_request.priority
    todo_model.complete=todo_request.complete

    db.add(todo_model)
    db.commit()

@router.delete("/todos/{todo_id}")
def delete_todo(user:user_dependency,db:db_dependency,todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication Failed")
    todo_model=db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get("id")[0]).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail="Item not found")
    db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get("id")).delete()
    db.commit()