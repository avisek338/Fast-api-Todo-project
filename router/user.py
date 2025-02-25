from typing import Annotated
from fastapi import APIRouter,Depends,Path,HTTPException
from models import Base,Todo,User
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from passlib.context import CryptContext
#from router.auth import router 
from .auth import get_current_user
router = APIRouter(prefix='/User',tags=['User'])

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RequestPhoneNumber(BaseModel):
    password:str
    phone_number:str



class RequestPassword(BaseModel):

    old_password:str 
    new_password:str = Field(min_length=3)


db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

@router.get('/user',status_code=status.HTTP_200_OK)
async def get_user(db:db_dependency,user:user_dependency):
    UserInfo = db.query(User).filter_by(id = user.get('id')).first()
    return UserInfo

@router.put('/user/passwordchange')
async def change_password(db:db_dependency,user:user_dependency,requestpassword:RequestPassword):
    old_password = requestpassword.old_password
    new_password = requestpassword.new_password
    request_user = db.query(User).filter_by(id = user.get('id')).first()
    if request_user is not None and bcrypt_context.verify(old_password,request_user.hashed_password):
        request_user.hashed_password = bcrypt_context.hash(new_password)
        db.add(request_user)
        db.commit()
        return {'message':'password changed successfully'}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='invalid password')
    
    
@router.put('/user/phone_number',status_code=status.HTTP_200_OK)
async def update_phone_number(db:db_dependency,requestnumber:RequestPhoneNumber,user:user_dependency):
    password = requestnumber.password
    phone_number = requestnumber.phone_number
    user_model  = db.query(User).filter_by(id = user.get('id')).first()

    if user_model is not None and bcrypt_context.verify(password,user_model.hashed_password):
        user_model.phone_number = phone_number
        db.add(user_model)
        db.commit()
        return {'message':'phone number has been updated'}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='invalid password')

    
    
    


    


