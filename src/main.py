import sys
import os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QDialog, QApplication, QListWidget, QPushButton, QLabel, QListWidgetItem, QVBoxLayout, QHBoxLayout, QFrame
import string
from PyQt5.QtCore import QSize

from sqlalchemy import select
from models.secret import Secret
from models.utils import *
from encrpytion.encryption import Encryption

class LoginScreen(QDialog):
    def __init__(self, stacked_widget) -> None:
        super(LoginScreen, self).__init__()
        self.stacked_widget = stacked_widget
        self.stacked_widget.setWindowTitle('Password Manager')
        loadUi('src/views/login.ui', self)
        self.passwordField.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginButton.clicked.connect(self.login)

    def login(self):
        password = self.passwordField.text()
        # delete later
        main_screen = MainScreen(self, self.stacked_widget, password)
        self.stacked_widget.addWidget(main_screen)
        self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)

        if not self.is_proper_password(password):
            self.passwordError.setText(f"Input at least 8 characters, smaller and upper letters and at least one digit")
        elif validate_master_password(password):
            main_screen = MainScreen(self, self.stacked_widget, password)
            self.stacked_widget.addWidget(main_screen)
            self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)
        else:
            self.passwordError.setText("Incorrect password")

    def is_proper_password(self, password):
        if len(password) < 8:
            return False
        
        lowercase_letters = string.ascii_lowercase
        uppercase_letters = string.ascii_uppercase
        digits = string.digits

        has_lower = False
        has_upper = False
        has_digit = False

        for char in password:
            if not has_lower and char in lowercase_letters:
                has_lower = True
            elif not has_upper and char in uppercase_letters:
                has_upper = True
            elif not has_digit and char in digits:
                has_digit = True

            if has_lower and has_upper and has_digit:
                return True
        
        return False

class MainScreen(QDialog):
    def __init__(self, parent, stacked_widget, password) -> None:
        super(MainScreen, self).__init__(parent)
        self.stacked_widget = stacked_widget
        self.list_widget = QListWidget(self)
        self.list_widget.setSpacing(5)
        self.setStyleSheet('background-color: rgb(61, 56, 70);')

        for i in range(100):
            my = SecretWidget(self, 'name', 'login', 'pass')
            list_item = QListWidgetItem(self.list_widget)
            list_item.setSizeHint(my.sizeHint())
            self.list_widget.addItem(list_item)
            self.list_widget.setItemWidget(list_item, my)

        layout = QVBoxLayout()
        descriptions_layout = QHBoxLayout()
        descriptions_layout.addWidget(QLabel('Name'))
        descriptions_layout.addWidget(QLabel('Login'))
        descriptions_layout.addWidget(QLabel('Password'))
        layout.addLayout(descriptions_layout)
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

class SecretWidget(QWidget):
    def __init__(self, parent, name, login, password):
        super(SecretWidget, self).__init__(parent)
        self.mylayout = QHBoxLayout()
        self.up = QLabel(name)
        self.middle = QLabel(login)
        self.down = QLabel(password)
        self.setStyleSheet('color: white')

        self.mylayout.addWidget(self.up,1)
        self.mylayout.addWidget(self.middle,1)
        self.mylayout.addWidget(self.down,1)

        self.setLayout(self.mylayout)

def testUI():
    app = QApplication(sys.argv)
    stacked_widget = QtWidgets.QStackedWidget()
    login = LoginScreen(stacked_widget)
    stacked_widget.addWidget(login)
    stacked_widget.setFixedWidth(1200)
    stacked_widget.setFixedHeight(800)
    stacked_widget.show()
    app.exec()

def test_backend():
    create_db()
    master_password = 'Password1!'

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




if __name__ == '__main__':
    testUI()
    #test_backend()

    # app = QApplication([])
    # window = MainWindow()
    # window.show()
    # app.exec_()

