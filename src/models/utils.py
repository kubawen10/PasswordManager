from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
import os
import string
import random

from encrpytion.encryption import Encryption
from . import base
from . import secret

def get_db_file() -> str:
    bd_directory = os.path.expanduser('~/.password_manager')

    if not os.path.exists(bd_directory):
        os.makedirs(bd_directory)

    return bd_directory + '/password_manager.sqlite3'

def get_engine():
    return create_engine('sqlite:///'+ get_db_file(), echo=False)

def get_session():
    return Session(get_engine())

def create_db():
    with get_session() as session:
        base.Base.metadata.create_all(get_engine())
        session.commit()

def validate_master_password(password: str) -> None:
    create_db()
    statement = select(secret.Secret.password)

    with get_session() as session:
        result = session.execute(statement).first()

    if result is None:
        return True
    else:
        try:
            encryptor = Encryption(password)
            encryptor.decrypt(result.password)
            return True
        except:
            return False
        
def generate_password(small_letters: bool, capital_letters: bool, digits: bool, special_chars: bool, length: int) -> str:
    alphabet = ""

    if small_letters:
        alphabet += string.ascii_lowercase

    if capital_letters:
        alphabet += string.ascii_uppercase
    
    if digits:
        alphabet += string.digits

    if special_chars:
        alphabet += string.punctuation

    return "".join(random.sample(alphabet, length))


