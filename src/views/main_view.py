from PyQt5.QtWidgets import QDialog, QStackedWidget, QListWidget, QPushButton, QHBoxLayout, QLabel, QVBoxLayout, QListWidgetItem, QWidget, QLineEdit, QMessageBox, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
import json
import os
import pyperclip

from utils.ui_utils import get_ui_file, get_icon_file
from models.secret import Secret
from models.queries import get_all_secrets, delete_secret
from .secret_form_view import SecretFormView


class MainView(QDialog):
    def __init__(self, stacked_widget: QStackedWidget, master_password: str) -> None:
        super(MainView, self).__init__()
        self.stacked_widget = stacked_widget
        self.master_password = master_password

        loadUi(get_ui_file('mainView.ui'), self)
        self.add_secret_button: QPushButton = self.findChild(QPushButton, 'addSecret')
        self.export_button: QPushButton = self.findChild(QPushButton, 'exportButton')
        self.list_of_secrets: QListWidget = self.findChild(QListWidget, 'listWidget')

        self.export_button.setToolTip('Export secrets to json file')

        self.list_of_secrets.setSpacing(5)
        self.list_of_secrets.setSelectionRectVisible(False)

        for secret in get_all_secrets():
            self.add_secret_to_list(secret)

        self.add_secret_button.clicked.connect(self.goto_add_secret_form)
        self.export_button.clicked.connect(self.export_secrets)


    def add_secret_to_list(self, secret: Secret) -> None:
        secret_widget = SecretWidget(self.list_of_secrets, self.stacked_widget, secret, self.master_password)
        list_item = QListWidgetItem(self.list_of_secrets)
        list_item.setSizeHint(secret_widget.sizeHint())
        self.list_of_secrets.addItem(list_item)
        self.list_of_secrets.setItemWidget(list_item, secret_widget)

    def goto_add_secret_form(self) -> None:
        form = SecretFormView(self, self.stacked_widget, self.master_password)
        self.stacked_widget.addWidget(form)
        self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)
    
    def export_secrets(self):
        list_of_secrets = [{'comment': 'remember that double quotes are preceded with backslash character in json so you need to remove them if you want to get the actual string'}]
        for index in range(self.list_of_secrets.count()):
            item = self.list_of_secrets.item(index)
            cur_secret: Secret = self.list_of_secrets.itemWidget(item).secret
            name, login, password, notes, date = cur_secret.get_decrypted_data(self.master_password)
            list_of_secrets.append({'name': name, 'login': login, 'password': password, 'notes': notes, 'modification_date': date})
          
        home_dir = os.path.expanduser('~')
        name = QFileDialog.getSaveFileName(self, 'Save file', home_dir, 'JSON Files (*.json)')
        file_name = name[0]

        if file_name != '' :
            with open(file_name, 'w', encoding='utf-8') as json_file:
                json.dump(list_of_secrets, json_file, indent=4, ensure_ascii=False)


class SecretWidget(QWidget):
    def __init__(self, parent: QListWidget, stacked_widget: QStackedWidget, secret: Secret, master_password: str):
        super(SecretWidget, self).__init__(parent)
        
        self.list_of_secrets = parent
        self.stacked_widget = stacked_widget
        self.master_password = master_password

        self.name_label = QLineEdit()
        self.name_label.setObjectName('name_label')
        self.login_label = QLineEdit()
        self.password_label = QLineEdit()

        self.name_label.setReadOnly(True)
        self.name_label.setFocusPolicy(False)
        self.login_label.setReadOnly(True)
        self.login_label.setFocusPolicy(False)
        self.password_label.setReadOnly(True)
        self.password_label.setFocusPolicy(False)
        self.password_label.setEchoMode(QLineEdit.Password)

        self.show_password_button = QPushButton()
        self.show_password_button.setIcon(QIcon(get_icon_file('show.png')))
        self.show_password_button.setCheckable(True)
        self.show_password_button.setToolTip('Show password')
        self.show_password_button.clicked.connect(self.set_password_visibility)

        self.copy_to_clipboard_button = QPushButton()
        self.copy_to_clipboard_button.setIcon(QIcon(get_icon_file('copy.png')))
        self.copy_to_clipboard_button.setToolTip('Copy password to clipboard')
        self.copy_to_clipboard_button.clicked.connect(self.copy_to_clipboard)

        self.show_notes_button = QPushButton()
        self.show_notes_button.setIcon(QIcon(get_icon_file('notes.png')))
        self.show_notes_button.setToolTip('Show secret notes')
        self.show_notes_button.clicked.connect(self.show_notes)

        self.update_secret_button = QPushButton()
        self.update_secret_button.setIcon(QIcon(get_icon_file('edit.png')))
        self.update_secret_button.setToolTip('Edit secret')
        self.update_secret_button.clicked.connect(self.goto_update_form)

        self.delete_secret_button = QPushButton()
        self.delete_secret_button.setIcon(QIcon(get_icon_file('delete.png')))
        self.delete_secret_button.setToolTip('Delete password')
        self.delete_secret_button.clicked.connect(self.delete_secret)

        for button in [self.show_password_button, self.copy_to_clipboard_button, self.show_notes_button, self.update_secret_button, self.delete_secret_button]:
            button.setStyleSheet('QPushButton{background-color: rgb(94, 92, 100); width: 26px; height: 26px; border-radius: 13px} QPushButton:hover{background-color: rgb(119, 118, 123);}')

        self.set_fields(secret)

        self.setStyleSheet('''
            QPushButton:hover{
                background-color: rgb(119, 118, 123);
            }

            QLineEdit {
                background-color: rgb(61, 56, 70);
                color: white;
                
            }

            QLineEdit#name_label {
                border: none;
            }

            QMessageBox {
                background-color: rgb(61, 56, 70);
            }
        
        ''')

        self.secret_layout = QHBoxLayout()
        self.secret_layout.addWidget(self.name_label,1)
        self.secret_layout.addWidget(self.login_label,1)
        self.secret_layout.addWidget(self.password_label,1)
        self.secret_layout.addWidget(self.show_password_button, 0)
        self.secret_layout.addWidget(self.copy_to_clipboard_button, 0)
        self.secret_layout.addWidget(self.show_notes_button, 0)
        self.secret_layout.addWidget(self.update_secret_button, 0)
        self.secret_layout.addWidget(self.delete_secret_button, 0)
        self.setLayout(self.secret_layout)


    def set_password_visibility(self, checked: bool) -> None:
        if checked:
            self.password_label.setEchoMode(QLineEdit.Normal)
            self.show_password_button.setIcon(QIcon(get_icon_file('hide.png')))
        else:
            self.password_label.setEchoMode(QLineEdit.Password)
            self.show_password_button.setIcon(QIcon(get_icon_file('show.png')))

    def copy_to_clipboard(self):
        pyperclip.copy(self.password_label.text())

    def show_notes(self):
        QMessageBox.information(self, 'Secret notes', self.notes)

    def goto_update_form(self) -> None:
        form = SecretFormView(self, self.stacked_widget, self.master_password, self.secret)
        self.stacked_widget.addWidget(form)
        self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)

    def delete_secret(self) -> None:
        confirm = QMessageBox.question(self, 'Confirm deletion', 'Are you sure you want to delete secret?')
        if confirm == QMessageBox.Yes:
            # delete secret from list of secrets in main view
            for index in range(self.list_of_secrets.count()):
                item = self.list_of_secrets.item(index)
                cur_secret = self.list_of_secrets.itemWidget(item).secret

                if cur_secret.id == self.secret.id:
                    self.list_of_secrets.takeItem(index)
                    break
            delete_secret(self.secret)

    def set_fields(self, secret: Secret) -> None:
        if self.show_password_button.isChecked():
            self.show_password_button.click()

        self.secret = secret
        name, login, password, notes, modification_time = self.secret.get_decrypted_data(self.master_password)
        
        self.name_label.setText(name)
        self.login_label.setText(login)
        self.password_label.setText(password)
        self.password_label.setToolTip('Modification time: ' + modification_time)
        self.notes = notes

        # add notes button text
    