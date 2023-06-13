from PyQt5.QtWidgets import QDialog, QStackedWidget, QLineEdit, QPushButton, QLabel
from PyQt5.uic import loadUi

from utils.password_utils import validate_master_password, is_proper_master_password
from utils.ui_utils import get_ui_file
from .main_view import MainView

class LoginView(QDialog):
    def __init__(self, stacked_widget: QStackedWidget) -> None:
        super(LoginView, self).__init__()
        self.stacked_widget = stacked_widget
        self.stacked_widget.setWindowTitle('Password Manager')
        
        loadUi(get_ui_file('login.ui'), self)
        self.password_field: QLineEdit = self.findChild(QLineEdit, 'passwordField')
        self.login_button: QPushButton = self.findChild(QPushButton, 'loginButton')
        self.password_error_label: QLabel = self.findChild(QLabel, 'passwordError')

        self.password_field.setEchoMode(QLineEdit.Password)
        self.login_button.clicked.connect(self.login)

    def login(self) -> None:
        master_password = self.passwordField.text()

        if not is_proper_master_password(master_password):
            self.password_error_label.setText(f"Input at least 8 characters, smaller and upper letters, digits and special characters")
        elif validate_master_password(master_password):
            main_screen = MainView(self.stacked_widget, master_password)
            self.stacked_widget.addWidget(main_screen)
            self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)
        else:
            self.password_error_label.setText("Incorrect password")
