from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
import os
import string
import random

from encrpytion.encryption import encrypt, decrypt
from . import base
from . import secret

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
        base.Base.metadata.create_all(get_engine())
        session.commit()


        



