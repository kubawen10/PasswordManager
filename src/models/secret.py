from typing import Any, Tuple
from sqlalchemy import Integer, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from encrpytion.encryption import encrypt, decrypt
from .base import Base

# try storing as one string described as len*string-of-len-charas ... eg 3*abc4*abcd...
class Secret(Base):
    __tablename__ = 'secret'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    secret_bytes: Mapped[bytes] = mapped_column(LargeBinary())

    def __init__(self, name:str, login: str, password: str, notes: str, master_password: str) -> None:
        creation_time_str = datetime.now().strftime('%d.%m.%Y %H:%M')
        self._encrypt_data(name, login, password, notes, creation_time_str, master_password)

    def _encrypt_data(self, name:str, login: str, password: str, notes: str, time: str,  master_password: str) -> None:
        joined_str = ''.join([self._get_string_with_len_prefix(field) for field in [name, login, password, notes, time]])
        self.secret_bytes = encrypt(joined_str, master_password)

    def _get_string_with_len_prefix(self, field: str) -> str:
        return str(len(field)) + '*' + field

    def get_decrypted_data(self, master_password: str) -> Tuple[str]:
        decrypted_joined_data = decrypt(self.secret_bytes, master_password)

        number_of_strings_to_retrieve = 5
        retrieved_strings = []

        for _ in range(number_of_strings_to_retrieve):
            separator_index = decrypted_joined_data.index('*')
            cur_str_length = int(decrypted_joined_data[:separator_index])
            decrypted_joined_data = decrypted_joined_data[separator_index+1:]
            cur_str = decrypted_joined_data[:cur_str_length]
            retrieved_strings.append(cur_str)
            decrypted_joined_data = decrypted_joined_data[cur_str_length:]

        return tuple(retrieved_strings)
    
    def update_data(self, name:str, login: str, password: str, notes: str, master_password: str) -> None:
        update_date = datetime.now().strftime('%d.%m.%Y %H:%M')
        self._encrypt_data(name, login, password, notes, update_date, master_password)
    
