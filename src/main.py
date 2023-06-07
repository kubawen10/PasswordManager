from models.utils import *
from encrpytion.encryption import Encryption
from sqlalchemy import select
from models.secret import Secret

if __name__ == '__main__':
    create_db()
    master_password = 'master'

    name = 'name'
    login = 'login'
    password = 'a' * 200
    notes = 'notes'

    e = Encryption(master_password)

    encrypted_password = e.encrypt(password)

    with get_session() as session:
        s = Secret(name, login, encrypted_password, notes)
        session.add(s)
        session.commit()

    with get_session() as session:
        statement = select(Secret)
        x = session.execute(statement).all()

    for i in x:
        p = i[0].password
        print(len(p))
        print(e.decrypt(p))

