from typing import Any
from sqlalchemy import Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column
from encrpytion.encryption import Encryption

from .base import Base
from .utils import get_session

# try storing as one string described as len*string-of-len-charas ... eg 3*abc4*abcd...
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
    
def add_new_secret(new_secret: Secret):
    with get_session() as session:
        session.add(new_secret)
        session.commit()

    with get_session() as session:
        return session.query(Secret).order_by(Secret.id.desc()).first()
    
def update_secret(secret_to_update: Secret, name:str, login: str, password: str, notes: str, master_password: str):
    secret_id = secret_to_update.id
    with get_session() as session:
        secret1 = session.query(Secret).get(secret_id)
        secret1.update_data(name, login, password, notes, master_password)
        session.commit()

    with get_session() as session:
        return session.query(Secret).get(secret_id)
        
def delete_secret(secret: Secret):
    with get_session() as session:
        session.delete(secret)
        session.commit()
        
def get_all_secrets():
    statement = select(Secret)
    with get_session() as session:
        result = session.execute(statement).all()

    return result