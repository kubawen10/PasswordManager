from typing import Any
from .base import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from encrpytion.encryption import Encryption

class Secret(Base):
    __tablename__ = 'secret'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String())
    login: Mapped[str] = mapped_column(String())
    password: Mapped[str] = mapped_column(String())
    notes: Mapped[str] = mapped_column(String())

    def __init__(self, name:str, login: str, password: str, notes: str, master_password: str) -> None:
        self._encrypt_data(name, login, password, notes, master_password)

    def _encrypt_data(self, name:str, login: str, password: str, notes: str, master_password: str):
        encryption = Encryption(master_password)

        self.name = encryption.encrypt(name)
        self.login = encryption.encrypt(login)
        self.password = encryption.encrypt(password)
        self.notes = encryption.encrypt(notes)

    def get_decrypted_data(self, master_password):
        encryption = Encryption(master_password)

        name = encryption.decrypt(self.name)
        login = encryption.decrypt(self.login)
        password = encryption.decrypt(self.password)
        notes = encryption.decrypt(self.notes)

        return name, login, password, notes
    
    def update_data(self, name:str, login: str, password: str, notes: str, master_password: str):
        self._encrypt_data(name, login, password, notes, master_password)

    def __repr__(self) -> str:
        return f'User(id={self.id!r} name={self.name!r} login={self.login!r})'