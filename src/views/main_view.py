from PyQt5.QtWidgets import QDialog, QStackedWidget, QListWidget, QPushButton, QHBoxLayout, QLabel, QVBoxLayout, QListWidgetItem, QWidget, QLineEdit, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
import os

from models.secret import Secret, get_all_secrets, delete_secret
from .secret_form_view import SecretFormView


class MainView(QDialog):
    def __init__(self, stacked_widget: QStackedWidget, master_password: str) -> None:
        super(MainView, self).__init__()
        self.stacked_widget = stacked_widget
        self.master_password = master_password

        loadUi(os.path.join(os.path.abspath(os.getcwd()),'src/uis/mainView.ui'), self)
        self.add_secret_button: QPushButton = self.findChild(QPushButton, 'addSecret')
        self.list_of_secrets: QListWidget = self.findChild(QListWidget, 'listWidget')

        self.list_of_secrets.setSpacing(5)

        for secret in get_all_secrets():
            self.add_secret_to_list(secret)

        self.add_secret_button.clicked.connect(self.goto_add_secret_form)


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
        self.show_password_button.setIcon(QIcon(os.path.join(os.path.abspath(os.getcwd()), 'src/uis/icons/show.png')))
        self.show_password_button.setCheckable(True)
        self.show_password_button.setToolTip('Show password')
        self.show_password_button.clicked.connect(self.set_password_visibility)

        self.copy_to_clipboard_button = QPushButton()
        self.copy_to_clipboard_button.setIcon(QIcon(os.path.join(os.path.abspath(os.getcwd()), 'src/uis/icons/copy.png')))
        self.copy_to_clipboard_button.setToolTip('Copy password to clipboard')

        self.show_notes_button = QPushButton()
        self.show_notes_button.setIcon(QIcon(os.path.join(os.path.abspath(os.getcwd()), 'src/uis/icons/notes.png')))
        self.show_notes_button.setToolTip('Show secret notes')

        self.update_secret_button = QPushButton()
        self.update_secret_button.setIcon(QIcon(os.path.join(os.path.abspath(os.getcwd()), 'src/uis/icons/edit.png')))
        self.update_secret_button.setToolTip('Edit secret')
        self.update_secret_button.clicked.connect(self.goto_update_form)

        self.delete_secret_button = QPushButton()
        self.delete_secret_button.setIcon(QIcon(os.path.join(os.path.abspath(os.getcwd()), 'src/uis/icons/delete.png')))
        self.delete_secret_button.setToolTip('Delete password')
        self.delete_secret_button.clicked.connect(self.delete_secret)

        self.set_fields(secret)

        self.setStyleSheet('''
            QPushButton#addSecret{
                background-color: rgb(94, 92, 100);
                border-radius: 13px;
                font: 20pt "Noto Mono";
                width: 26px;
                height: 26px;
            }

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
            self.show_password_button.setIcon(QIcon(os.path.join(os.path.abspath(os.getcwd()), 'src/uis/icons/hide.png')))
        else:
            self.password_label.setEchoMode(QLineEdit.Password)
            self.show_password_button.setIcon(QIcon(os.path.join(os.path.abspath(os.getcwd()), 'src/uis/icons/show.png')))

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

        # add notes button text
    