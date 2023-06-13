from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import os

from .base import Base
from .secret import Secret

def get_db_file() -> str:
    bd_directory = os.path.expanduser('~/.password_manager')

    if not os.path.exists(bd_directory):
        os.makedirs(bd_directory)

    return os.path.join(bd_directory , 'password_manager.sqlite3')

def get_engine():
    return create_engine('sqlite:///'+ get_db_file(), echo=False)

def get_session():
    return Session(bind=get_engine())

def create_db():
    with get_session() as session:
        Base.metadata.create_all(get_engine())
        session.commit()


        



