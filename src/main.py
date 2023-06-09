import sys
import os
import typing
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QDialog, QApplication, QListWidget, QPushButton, QLabel, QListWidgetItem, QVBoxLayout, QHBoxLayout, QFrame, QLineEdit, QStackedWidget
import string

from sqlalchemy import select
from models.secret import Secret
from models.utils import *
from encrpytion.encryption import Encryption

class LoginScreen(QDialog):
    def __init__(self, stacked_widget: QStackedWidget) -> None:
        super(LoginScreen, self).__init__()
        self.stacked_widget = stacked_widget
        self.stacked_widget.setWindowTitle('Password Manager')
        loadUi('src/views/login.ui', self)

        # TODO: add style hints for this, thera was yt tutorial for it
        self.passwordField.setEchoMode(QLineEdit.Password)
        self.loginButton.clicked.connect(self.login)

    def login(self):
        master_password = self.passwordField.text()

        if not self.is_proper_password(master_password):
            self.passwordError.setText(f"Input at least 8 characters, smaller and upper letters and at least one digit")
        elif validate_master_password(master_password):
            main_screen = MainScreen(self.stacked_widget, master_password)
            self.stacked_widget.addWidget(main_screen)
            self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)
        else:
            self.passwordError.setText("Incorrect password")

    def is_proper_password(self, master_password):
        if len(master_password) < 8:
            return False
        
        lowercase_letters = string.ascii_lowercase
        uppercase_letters = string.ascii_uppercase
        digits = string.digits

        has_lower = False
        has_upper = False
        has_digit = False

        for char in master_password:
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
    def __init__(self, stacked_widget: QStackedWidget, master_password: str) -> None:
        super(MainScreen, self).__init__()
        self.stacked_widget = stacked_widget
        self.master_password = master_password
        self.setStyleSheet('background-color: rgb(61, 56, 70);')

        self.list_widget = QListWidget(self)
        self.list_widget.setSpacing(5)

        for secret_tuple in get_all_secrets():
            self.add_secret_to_list(secret_tuple[0])

        self.add_new_secret = QPushButton('Add')
        self.add_new_secret.clicked.connect(self.goto_add_secret_form)
        
        descriptions_layout = QHBoxLayout()
        descriptions_layout.addWidget(QLabel('Name'))
        descriptions_layout.addWidget(QLabel('Login'))
        descriptions_layout.addWidget(QLabel('Password'))

        layout = QVBoxLayout()
        layout.addWidget(self.add_new_secret)
        layout.addLayout(descriptions_layout)
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

    def add_secret_to_list(self, secret: secret.Secret):
        secret_widget = SecretWidget(self, self.stacked_widget, secret, self.master_password)
        list_item = QListWidgetItem(self.list_widget)
        list_item.setSizeHint(secret_widget.sizeHint())
        self.list_widget.addItem(list_item)
        self.list_widget.setItemWidget(list_item, secret_widget)

    def goto_add_secret_form(self):
        form = SecretForm(self, self.stacked_widget, self.master_password)
        self.stacked_widget.addWidget(form)
        self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)

class SecretWidget(QWidget):
    def __init__(self, parent, stacked_widget: QStackedWidget, secret: Secret, master_password: str):
        super(SecretWidget, self).__init__(parent)
        self.setStyleSheet('color: white')
        self.stacked_widget = stacked_widget
        self.master_password = master_password

        self.id_label = QLabel()
        self.name_label = QLabel()
        self.login_label = QLineEdit()
        self.password_label = QLineEdit()
        
        self.set_fields(secret)

        self.login_label.setReadOnly(True)
        self.login_label.setFocusPolicy(False)

        self.password_label.setReadOnly(True)
        self.password_label.setFocusPolicy(False)
        self.password_label.setEchoMode(QLineEdit.Password)

        self.show_button = QPushButton('show')
        self.show_button.setCheckable(True)
        self.show_button.clicked.connect(self.set_password_visibility)

        self.update_button = QPushButton('update')
        self.update_button.clicked.connect(self.goto_update_form)

        self.secret_layout = QHBoxLayout()
        self.secret_layout.addWidget(self.id_label,0)
        self.secret_layout.addWidget(self.name_label,1)
        self.secret_layout.addWidget(self.login_label,1)
        self.secret_layout.addWidget(self.password_label,1)
        self.secret_layout.addWidget(self.show_button, 0)
        self.secret_layout.addWidget(self.update_button, 0)
        self.setLayout(self.secret_layout)

    def set_password_visibility(self, checked):
        if checked:
            self.password_label.setEchoMode(QLineEdit.Normal)
        else:
            self.password_label.setEchoMode(QLineEdit.Password)

    def goto_update_form(self):
        form = SecretForm(self, self.stacked_widget, self.master_password, self.secret)
        self.stacked_widget.addWidget(form)
        self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)

    def set_fields(self, secret):
        self.secret = secret
        name, login, password, notes = self.secret.get_decrypted_data(self.master_password)
        
        self.id_label.setText(str(self.secret.id))
        self.name_label.setText(name)
        self.login_label.setText(login)
        self.password_label.setText(password)
    
class SecretForm(QDialog):
    def __init__(self, parent, stacked_widget, master_password, secret: Secret | None = None) -> None:
        super(SecretForm, self).__init__(parent)
        self.parent_widget = parent
        self.stacked_widget = stacked_widget
        self.master_password = master_password
        self.secret = secret

        loadUi('src/views/secretForm.ui', self)

        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.showPasswordButton.setCheckable(True)
        self.showPasswordButton.clicked.connect(self.set_password_visibility)
        self.cancelButton.clicked.connect(self.exit_form)
        self.confirmButton.clicked.connect(self.confirm_button_clicked)

        if secret:
            self.dialogName.setText('Edit secret')
            self.confirmButton.setText('Apply')
            name, login, password, notes = self.secret.get_decrypted_data(self.master_password)
            self.nameEdit.setText(name)
            self.loginEdit.setText(login)
            self.passwordEdit.setText(password)
            self.notesEdit.setPlainText(notes)

        else:
            self.dialogName.setText('Add secret')
            self.confirmButton.setText('Add')

    def set_password_visibility(self, checked):
        if checked:
            self.passwordEdit.setEchoMode(QLineEdit.Normal)
        else:
            self.passwordEdit.setEchoMode(QLineEdit.Password)

    def confirm_button_clicked(self):
        if not self.validate_inputs():
            self.validationError.setText("Name, login and password cannot be empty.")

        elif self.secret:
            updated_secret = update_secret(self.secret, self.nameEdit.text(), self.loginEdit.text(), self.passwordEdit.text(), self.notesEdit.toPlainText(), self.master_password)
            self.parent_widget.set_fields(updated_secret)
            self.exit_form()
        else:
            new_secret = Secret(self.nameEdit.text(), self.loginEdit.text(), self.passwordEdit.text(), self.notesEdit.toPlainText(), self.master_password)
            added_secret = add_new_secret(new_secret)
            self.parent_widget.add_secret_to_list(added_secret)
            self.exit_form()

    def validate_inputs(self):
        if len(self.nameEdit.text()) == 0:
            return False
        if len(self.loginEdit.text()) == 0:
            return False
        if len(self.passwordEdit.text()) == 0:
            return False
        return True

    def exit_form(self):
        self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex()-1)
        self.stacked_widget.removeWidget(self)

def testUI():
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()
    login = LoginScreen(stacked_widget)
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


