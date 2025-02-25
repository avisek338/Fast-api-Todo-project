from typing import Annotated
from fastapi import APIRouter,Depends,Path,HTTPException
from models import Base,Todo
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
#from router.auth import router 
from .auth import get_current_user
router = APIRouter()


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

@router.get('/todos',status_code=status.HTTP_200_OK)
async def get_todos(db: db_dependency,user:user_dependency):
    todos = db.query(Todo).filter_by(owner_id = user.get('id')).all()
    return todos

@router.get('/todos/{todo_id}',status_code=status.HTTP_200_OK)
async def get_todo(user:user_dependency,db:db_dependency,todo_id:int = Path(gt = 0)):
    todo = db.query(Todo).filter_by(id = todo_id,owner_id = user.get('id')).first()
    if todo is not None:
        return todo
    raise HTTPException(404,f'item not found with id {todo_id}')


@router.post('/todos',status_code=status.HTTP_201_CREATED)
async def create_todo(user:user_dependency,db:db_dependency,todo_request:TodoRequest):
    new_todo  = Todo(**todo_request.model_dump(),owner_id = user['id'])
    db.add(new_todo)
    db.commit()

@router.put('/todos/{todo_id}',status_code=status.HTTP_200_OK)
def update_todo(user:user_dependency,db:db_dependency,todo_request:TodoRequest,todo_id:int = Path(gt=0)):
    todo = db.query(Todo).filter_by(id = todo_id,owner_id = user.get('id')).first()
    if not todo:
         raise HTTPException(404,f'item not found with id {todo_id}')
    todo.title = todo_request.title
    todo.description = todo_request.description
    todo.priority = todo_request.priority
    todo.complete = todo_request.complete
    db.add(todo)
    db.commit()


@router.delete('/todos/{todo_id}')
async def delete_todo(user:user_dependency,db:db_dependency,todo_id:int = Path(gt=0)):
    todo = db.query(Todo).filter_by(id = todo_id,owner_id = user.get('id')).first()
    if todo is None:
        raise HTTPException(status_code=404,detail=f'Item not found with id {todo_id}')
    db.delete(todo)
    db.commit()

     









