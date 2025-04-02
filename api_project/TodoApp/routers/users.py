from typing import Annotated
from fastapi import Depends,APIRouter, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
router=APIRouter()
from models import Users
from .auth import get_current_user
from passlib.context import CryptContext

router=APIRouter(prefix="/users",tags=["user"])

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserRequest(BaseModel):
   password:str
   new_password:str=Field(min_length=6)


db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]
bcrypt_context=CryptContext(schemes=["bcrypt"],deprecated="auto")


@router.get("/",status_code=status.HTTP_200_OK)
def read_user(db:db_dependency,user:user_dependency):
   if user is None:
       raise HTTPException(status_code=404,detail="User not found")
   return db.query(Users).filter(Users.id==user.get("id")[0]).first()

@router.put("/update_user_details",status_code=status.HTTP_204_NO_CONTENT)
def update_user_details(db:db_dependency,user:user_dependency,user_request:UserRequest):
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    user_model= db.query(Users).filter(Users.id==user.get("id")[0]).first()
    if user_model is  None:
        raise HTTPException(status_code=404,detail="User not found")
    if not bcrypt_context.verify(user_request.password,user_model.hashed_password):
        raise HTTPException(status_code=400,detail="Error on password change")
    user_model.hashed_password=bcrypt_context.hash(user_request.new_password)
    db.add(user_model)
    db.commit()

