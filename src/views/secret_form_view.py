from PyQt5.QtWidgets import QDialog, QLineEdit, QStackedWidget, QPushButton, QTextEdit, QLabel
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon

from models.secret import Secret
from models.queries import add_new_secret, update_secret
from .password_generator_form_view import PasswordGeneratorFormView
from utils.ui_utils import get_ui_file, get_icon_file

class SecretFormView(QDialog):
    def __init__(self, parent, stacked_widget: QStackedWidget, master_password: str, secret: Secret | None = None) -> None:
        super(SecretFormView, self).__init__(parent)
        self.parent_widget = parent
        self.stacked_widget = stacked_widget
        self.master_password = master_password
        self.secret = secret

        loadUi(get_ui_file('secretForm.ui'), self)
        self.form_title: QLabel = self.findChild(QLabel, 'dialogName')
        self.name_field: QLineEdit = self.findChild(QLineEdit, 'nameEdit')
        self.login_field: QLineEdit = self.findChild(QLineEdit, 'loginEdit')
        self.password_field: QLineEdit = self.findChild(QLineEdit, 'passwordEdit')
        self.notes_field: QTextEdit = self.findChild(QTextEdit, 'notesEdit')
        self.validation_error_label: QLabel = self.findChild(QLabel, 'validationError')
        self.show_password_button: QPushButton = self.findChild(QPushButton, 'showPasswordButton')
        self.generate_password_button: QPushButton = self.findChild(QPushButton, 'generatePasswordButton')
        self.cancel_button: QPushButton = self.findChild(QPushButton, 'cancelButton')
        self.confirm_button: QPushButton = self.findChild(QPushButton, 'confirmButton')

        self.show_password_button.setIcon(QIcon(get_icon_file('show.png')))
        self.generate_password_button.setIcon(QIcon(get_icon_file('generate.png')))

        self.password_field.setEchoMode(QLineEdit.Password)
        self.show_password_button.setCheckable(True)
        self.show_password_button.clicked.connect(self.set_password_visibility)
        self.generate_password_button.clicked.connect(self.goto_password_generator)
        self.cancel_button.clicked.connect(self.exit_form)
        self.confirm_button.clicked.connect(self.confirm_button_clicked)

        # if secret is profided, form's purpose is to edit secret, else it's purpose is to add new secret
        if secret:
            self.form_title.setText('Edit secret')
            self.confirm_button.setText('Apply')
            name, login, password, notes, _ = self.secret.get_decrypted_data(self.master_password)
            self.name_field.setText(name)
            self.login_field.setText(login)
            self.password_field.setText(password)
            self.notes_field.setPlainText(notes)

        else:
            self.form_title.setText('Add secret')
            self.confirm_button.setText('Add')

    def set_password_visibility(self, checked: bool):
        if checked:
            self.password_field.setEchoMode(QLineEdit.Normal)
            self.show_password_button.setIcon(QIcon(get_icon_file('hide.png')))
        else:
            self.password_field.setEchoMode(QLineEdit.Password)
            self.show_password_button.setIcon(QIcon(get_icon_file('show.png')))

    def set_generated_password(self, password):
        if self.show_password_button.isChecked():
            self.show_password_button.click()
        
        self.password_field.setText(password)

    def goto_password_generator(self):
        form = PasswordGeneratorFormView(self, self.stacked_widget)
        self.stacked_widget.addWidget(form)
        self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)


    def confirm_button_clicked(self):
        if not self.validate_inputs():
            self.validation_error_label.setText("Name, login and password cannot be empty.")
        
        # if secret is provided, update the SecretWidget, else add new secret to the list
        elif self.secret:
            updated_secret = update_secret(self.secret, self.name_field.text(), self.login_field.text(), self.password_field.text(), self.notes_field.toPlainText(), self.master_password)
            self.parent_widget.set_fields(updated_secret)
            self.exit_form()
        else:
            new_secret = Secret(self.name_field.text(), self.login_field.text(), self.password_field.text(), self.notes_field.toPlainText(), self.master_password)
            added_secret = add_new_secret(new_secret)
            self.parent_widget.add_secret_to_list(added_secret)
            self.exit_form()

    def validate_inputs(self):
        if len(self.name_field.text()) == 0:
            return False
        if len(self.login_field.text()) == 0:
            return False
        if len(self.password_field.text()) == 0:
            return False
        return True

    def exit_form(self):
        self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex()-1)
        self.stacked_widget.removeWidget(self)