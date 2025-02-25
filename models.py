from database import Base
from sqlalchemy import String,Integer,Boolean,Column,ForeignKey


class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean,default=False)
    owner_id = Column(Integer,ForeignKey('users.id'))


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String,unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean,default=False)
    role = Column(String)
    phone_number = Column(String)



