from PyQt5.QtWidgets import QDialog, QStackedWidget, QLineEdit
from PyQt5.uic import loadUi
import string

from models.utils import validate_master_password
from .main_view import MainView

class LoginView(QDialog):
    def __init__(self, stacked_widget: QStackedWidget) -> None:
        super(LoginView, self).__init__()
        self.stacked_widget = stacked_widget
        self.stacked_widget.setWindowTitle('Password Manager')
        loadUi('src/uis/login.ui', self)

        # TODO: add style hints for this, thera was yt tutorial for it
        self.passwordField.setEchoMode(QLineEdit.Password)
        self.loginButton.clicked.connect(self.login)

    def login(self) -> None:
        master_password = self.passwordField.text()

        if not self.is_proper_password(master_password):
            self.passwordError.setText(f"Input at least 8 characters, smaller and upper letters and at least one digit")
        elif validate_master_password(master_password):
            main_screen = MainView(self.stacked_widget, master_password)
            self.stacked_widget.addWidget(main_screen)
            self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)
        else:
            self.passwordError.setText("Incorrect password")

    def is_proper_password(self, master_password: str) -> bool:
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