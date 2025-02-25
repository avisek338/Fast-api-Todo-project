from typing import Annotated
from fastapi import FastAPI,Depends,Path,HTTPException
from models import Base,Todo
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from router.auth import router as authrouter
from router.todos import router as todorouter
from router.admin import router as adminrouter
from router.user import router as userrouter


app = FastAPI()


#Base.metadata.drop_all(bind=engine)
#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app.include_router(authrouter)
app.include_router(todorouter)
app.include_router(adminrouter)
app.include_router(userrouter)

