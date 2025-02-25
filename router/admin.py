from typing import Annotated
from fastapi import APIRouter,Depends,Path,HTTPException
from models import Base,Todo
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from passlib.context import CryptContext
#from router.auth import router 
from .auth import get_current_user
router = APIRouter(prefix='/admin',tags=['admin'])

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TodoRequest(BaseModel):

    title :str = Field(min_length=3,max_length=100)
    description : str = Field(max_length=100)
    priority : int = Field(gt=0,lt=6)
    complete :bool 


db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

@router.get('/todos')
async def get_all_todos(user:user_dependency,db:db_dependency):
    if user.get('role') == 'admin':
        todos = db.query(Todo).all()
        return todos
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Unauthorized User')

@router.delete('/todos/{todo_id}')
async def delete_todo(user:user_dependency,db:db_dependency,todo_id:int = Path(gt=0)):
    if user.get('role') == 'admin':
        todos = db.query(Todo).filter_by(id = todo_id).first()
        db.delete(todos)
        db.commit()
        return {'message':'successfully deleted'}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Unauthorized User')
    



