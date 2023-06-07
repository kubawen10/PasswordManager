from typing import Any
from base import Base
from utils import *
from sqlalchemy import Integer, String, select, literal
from sqlalchemy.orm import Mapped, mapped_column
from Crypto.Hash import SHA256

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64))
    password: Mapped[str] = mapped_column(String(64))

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = self._hash_password(password)
        
    def _hash_password(self, password: str):
        return SHA256.new(password.encode()).hexdigest()
    
    def __repr__(self) -> str:
        return f'User(id={self.id!r} username={self.username!r} password={self.password!r})'
    
    
def username_exists(username: str):
    session = get_session()
    query = session.query(User).filter_by(username=username)
    return session.query(query.exists()).scalar()

    
def add(username: str, password: str) -> bool:
    if username_exists(username):
        return False
    with get_session() as session:
        user = User(username, password)
        session.add(user)
        session.commit()
    return True

def get_all():
    with get_session() as session:
        statement = select(User)
        return session.execute(statement).all()
