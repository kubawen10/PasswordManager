from PyQt5.QtWidgets import QDialog, QStackedWidget, QCheckBox, QPushButton, QLabel
from PyQt5.uic import loadUi

import os
from utils.password_utils import generate_password

class PasswordGeneratorFormView(QDialog):
    def __init__(self, parent, stacked_widget: QStackedWidget) -> None:
        super(PasswordGeneratorFormView, self).__init__(parent)
        self.parent_widget = parent
        self.stacked_widget = stacked_widget

        loadUi(os.path.join(os.path.abspath(os.getcwd()), 'src/uis/passwordGeneratorForm.ui'), self)
        self.small_letters_checkbox: QCheckBox = self.findChild(QCheckBox, 'smallLetters')
        self.capital_letters_checkbox: QCheckBox = self.findChild(QCheckBox, 'capitalLetters')
        self.digits_checkbox: QCheckBox = self.findChild(QCheckBox, 'digits')
        self.special_chars_checkbox: QCheckBox = self.findChild(QCheckBox, 'specialChars')
        self.generate_password_button: QPushButton = self.findChild(QPushButton, 'generateButton')
        self.generation_error_label: QLabel = self.findChild(QLabel, 'generationError')
        self.password_length_label: QLabel = self.findChild(QLabel, 'passwordLength')

        self.bgWidget.setStyleSheet('''
            QCheckBox{{
                color: rgb(255, 255, 255);
                font: 20pt "Noto Mono";
            }}

            QCheckBox:hover{{
                color: rgb(200, 200, 200);
            }}

            QCheckBox::indicator:checked{{
                image: url({0})
            }}

            QCheckBox::indicator:unchecked{{
                image: url({1})
            }}
        
        '''.format(os.path.join(os.path.abspath(os.getcwd()), 'src/uis/icons/checked.png'), 
                   os.path.join(os.path.abspath(os.getcwd()), 'src/uis/icons/unchecked.png')))

        self.generate_password_button.clicked.connect(self.generate)

    def generate(self):
        if not self.validate_checkboxes():
            self.generation_error_label.setText("Pick at least one checkbox.")
        else:
            small_checked = self.small_letters_checkbox.isChecked()
            capital_checked = self.capital_letters_checkbox.isChecked()
            digits_checked = self.digits_checkbox.isChecked()
            special_checked = self.special_chars_checkbox.isChecked()
            password_length = int(self.password_length_label.text())

            password = generate_password(small_checked, capital_checked, digits_checked, special_checked, password_length)

            self.parent_widget.set_generated_password(password)

            self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex()-1)
            self.stacked_widget.removeWidget(self)

    def validate_checkboxes(self):
        small_checked = self.small_letters_checkbox.isChecked()
        capital_checked = self.capital_letters_checkbox.isChecked()
        digits_checked = self.digits_checkbox.isChecked()
        special_checked = self.special_chars_checkbox.isChecked()

        return small_checked or capital_checked or digits_checked or special_checked
            