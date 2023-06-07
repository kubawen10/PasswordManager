from typing import Any
from .base import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Secret(Base):
    __tablename__ = 'secret'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    login: Mapped[str] = mapped_column(String(128))
    # max length of password provided is 128
    password: Mapped[str] = mapped_column(String(192))
    notes: Mapped[str] = mapped_column(String(512))

    def __init__(self, name:str, login: str, password: str, notes: str) -> None:
        self.name = name
        self.login = login
        self.password = password
        self.notes = notes
    
    def __repr__(self) -> str:
        return f'User(id={self.id!r} name={self.name!r} login={self.login!r})'