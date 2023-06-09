from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
import os
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

def validate_master_password(password):
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
        
def add_new_secret(new_secret):
    with get_session() as session:
        session.add(new_secret)
        session.commit()

    with get_session() as session:
        return session.query(secret.Secret).order_by(secret.Secret.id.desc()).first()
    
def update_secret(secret_to_update, name:str, login: str, password: str, notes: str, master_password: str):
    secret_id = secret_to_update.id
    with get_session() as session:
        secret1 = session.query(secret.Secret).get(secret_id)
        secret1.update_data(name, login, password, notes, master_password)
        session.commit()

    with get_session() as session:
        return session.query(secret.Secret).get(secret_id)
        
def delete_secret(secret):
    with get_session() as session:
        session.delete(secret)
        session.commit()
        
def get_all_secrets():
    statement = select(secret.Secret)
    with get_session() as session:
        result = session.execute(statement).all()

    return result

