import sys
import os
import typing

from PyQt5.QtWidgets import QApplication, QStackedWidget

from sqlalchemy import select
from models.secret import Secret
from models.utils import *
from views.login_view import LoginView


def testUI():
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()
    login = LoginView(stacked_widget)
    stacked_widget.addWidget(login)
    stacked_widget.setFixedWidth(1200)
    stacked_widget.setFixedHeight(800)
    stacked_widget.show()
    app.exec()

def test_backend():
    create_db()
    master_password = 'Password1!'

    # name = 'namexd'
    # login = 'logindx'
    # password = 'passworddd'
    # notes = 'notesss'

    # with get_session() as session:
    #     s = Secret(name, login, password, notes, master_password)
    #     session.add(s)
    #     session.commit()

    with get_session() as session:
        statement = select(Secret)
        x = session.execute(statement).all()

    for i in x:
        print(i[0].get_decrypted_data(master_password))

    for i in x:
        i[0].update_data('jakis', 'nowy', 'sadf', 'notes', master_password)

    for i in x:
        print(i[0].get_decrypted_data(master_password))

    with get_session() as session:
        session.commit()


    with get_session() as session:
        statement = select(Secret)
        x = session.execute(statement).all()

    for i in x:
        print(i[0].get_decrypted_data(master_password))

if __name__ == '__main__':
    testUI()
    #test_backend()


