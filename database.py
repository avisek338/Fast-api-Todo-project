
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
load_dotenv()

SQLALCHEMY_DATABSE_URI =os.getenv('DATABSE_URI')


engine = create_engine(SQLALCHEMY_DATABSE_URI)
SessionLocal = sessionmaker(autoflush=False,autocommit = False,bind = engine)
Base = declarative_base()





