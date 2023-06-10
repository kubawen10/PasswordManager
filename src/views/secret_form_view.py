from PyQt5.QtWidgets import QDialog, QLineEdit, QStackedWidget
from PyQt5.uic import loadUi

from models.secret import Secret, add_new_secret, update_secret
from .password_generator_form_view import PasswordGeneratorFormView

class SecretFormView(QDialog):
    def __init__(self, parent, stacked_widget: QStackedWidget, master_password: str, secret: Secret | None = None) -> None:
        super(SecretFormView, self).__init__(parent)
        self.parent_widget = parent
        self.stacked_widget = stacked_widget
        self.master_password = master_password
        self.secret = secret

        loadUi('src/uis/secretForm.ui', self)

        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.showPasswordButton.setCheckable(True)
        self.showPasswordButton.clicked.connect(self.set_password_visibility)
        self.generatePasswordButton.clicked.connect(self.goto_password_generator)
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

    def set_generated_password(self, password):
        if self.showPasswordButton.isChecked():
            self.showPasswordButton.click()
        
        self.passwordEdit.setText(password)

    def goto_password_generator(self):
        form = PasswordGeneratorFormView(self, self.stacked_widget)
        self.stacked_widget.addWidget(form)
        self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)


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