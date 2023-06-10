from PyQt5.QtWidgets import QDialog, QStackedWidget
from PyQt5.uic import loadUi
from models.utils import generate_password

class PasswordGeneratorFormView(QDialog):
    def __init__(self, parent, stacked_widget: QStackedWidget) -> None:
        super(PasswordGeneratorFormView, self).__init__(parent)
        self.parent_widget = parent
        self.stacked_widget = stacked_widget

        loadUi('src/uis/passwordGeneratorForm.ui', self)

        self.generateButton.clicked.connect(self.generate)

    def generate(self):
        if not self.validate_checkboxes():
            self.generationError.setText("Pick at least one checkbox.")
        else:
            small_checked = self.smallLetters.isChecked()
            capital_checked = self.capitalLetters.isChecked()
            digits_checked = self.digits.isChecked()
            special_checked = self.specialChars.isChecked()
            password_length = int(self.passwordLength.text())

            password = generate_password(small_checked, capital_checked, digits_checked, special_checked, password_length)

            self.parent_widget.set_generated_password(password)

            self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex()-1)
            self.stacked_widget.removeWidget(self)

        


    def validate_checkboxes(self):
        small_checked = self.smallLetters.isChecked()
        capital_checked = self.capitalLetters.isChecked()
        digits_checked = self.digits.isChecked()
        special_checked = self.specialChars.isChecked()

        return small_checked or capital_checked or digits_checked or special_checked
            