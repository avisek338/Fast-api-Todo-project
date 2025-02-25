from typing import Annotated
from fastapi import APIRouter,Depends,Path,HTTPException
from models import Todo,User
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
load_dotenv()
router = APIRouter(prefix='/auth',tags=['auth'])

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")





SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserRequest(BaseModel):

    email :str 
    first_name:str
    last_name :str
    password :str = Field(min_length=4)
    is_active :bool
    role :str
    phone_number:str

class LoginRequest(BaseModel):
    email:str
    password:str    

class Token(BaseModel):
    access_token: str
    token_type: str


    


db_dependency = Annotated[Session,Depends(get_db)]

#helper functions
def authenicate_user(db,password:str,email:str):
    user = db.query(User).filter_by(email = email).first()
    if user is not None and bcrypt_context.verify(password,user.hashed_password):
        return user
    else :
        return None
    
def create_access_token(username:str,user_id:int, role:str,expires_delta: timedelta | None):
    to_encode = {'sub':username,'id':user_id,'role':role}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token:Annotated[str,Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        if payload.get('sub') == None :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user')
        else:
            return {'username': payload.get('sub'),'id':payload.get('id'),'role':payload.get('role')}
    except :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate user')
        




      


#routes

@router.post('/user',status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,user_request:UserRequest):
    user = User(
      email = user_request.email,
      first_name = user_request.first_name,
      last_name  = user_request.last_name,
      hashed_password = bcrypt_context.hash(user_request.password),
      is_active = True,
      role = user_request.role
    )
    db.add(user)
    db.commit()
    return {'message':'user created'}

@router.post('/token',status_code=status.HTTP_200_OK,response_model=Token)
async def login_for_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    user = authenicate_user(db,form_data.password,form_data.username)
    if not user:
        return {'message':'authenication failed'}

    token =  create_access_token(user.email,user.id,user.role,timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) 
    return Token(access_token=token,token_type='bearer')

        
    










