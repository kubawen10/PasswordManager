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
        self.listWidget.setSpacing(5)

        for secret_tuple in get_all_secrets():
            self.add_secret_to_list(secret_tuple[0])

        self.addSecret.clicked.connect(self.goto_add_secret_form)


    def add_secret_to_list(self, secret: Secret) -> None:
        secret_widget = SecretWidget(self.listWidget, self, self.stacked_widget, secret, self.master_password)
        list_item = QListWidgetItem(self.listWidget)
        list_item.setSizeHint(secret_widget.sizeHint())
        self.listWidget.addItem(list_item)
        self.listWidget.setItemWidget(list_item, secret_widget)

    def delete_secret_from_list(self, secret: Secret) -> None:
        for index in range(self.listWidget.count()):
            item = self.listWidget.item(index)
            cur_secret = self.listWidget.itemWidget(item).secret

            if cur_secret.id == secret.id:
                self.listWidget.takeItem(index)
                break

    def goto_add_secret_form(self) -> None:
        form = SecretFormView(self, self.stacked_widget, self.master_password)
        self.stacked_widget.addWidget(form)
        self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)


class SecretWidget(QWidget):
    def __init__(self, parent: QListWidget, mainWiev: MainView, stacked_widget: QStackedWidget, secret: Secret, master_password: str):
        super(SecretWidget, self).__init__(parent)
        
        self.mainWiev = mainWiev
        self.stacked_widget = stacked_widget
        self.master_password = master_password

        # TODO: delete id later
        self.id_label = QLabel()
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

        self.show_button = QPushButton()
        self.show_button.setIcon(QIcon(os.path.join(os.path.abspath(os.getcwd()), 'src/uis/icons/show.png')))
        self.show_button.setCheckable(True)
        self.show_button.setToolTip('Show password')
        self.show_button.clicked.connect(self.set_password_visibility)

        self.copy_to_clipboard_button = QPushButton()
        self.copy_to_clipboard_button.setIcon(QIcon(os.path.join(os.path.abspath(os.getcwd()), 'src/uis/icons/copy.png')))
        self.copy_to_clipboard_button.setToolTip('Copy password to clipboard')

        self.show_notes_button = QPushButton()
        self.show_notes_button.setIcon(QIcon(os.path.join(os.path.abspath(os.getcwd()), 'src/uis/icons/notes.png')))
        self.show_notes_button.setToolTip('Show secret notes')

        self.update_button = QPushButton()
        self.update_button.setIcon(QIcon(os.path.join(os.path.abspath(os.getcwd()), 'src/uis/icons/edit.png')))
        self.update_button.setToolTip('Edit secret')
        self.update_button.clicked.connect(self.goto_update_form)

        self.delete_button = QPushButton()
        self.delete_button.setIcon(QIcon(os.path.join(os.path.abspath(os.getcwd()), 'src/uis/icons/delete.png')))
        self.delete_button.setToolTip('Delete password')
        self.delete_button.clicked.connect(self.delete_secret)

        self.set_fields(secret)

        self.setStyleSheet('''
            QPushButton{
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
        
        ''')

        self.secret_layout = QHBoxLayout()
        self.secret_layout.addWidget(self.id_label,0)
        self.secret_layout.addWidget(self.name_label,1)
        self.secret_layout.addWidget(self.login_label,1)
        self.secret_layout.addWidget(self.password_label,1)
        self.secret_layout.addWidget(self.show_button, 0)
        self.secret_layout.addWidget(self.copy_to_clipboard_button, 0)
        self.secret_layout.addWidget(self.show_notes_button, 0)
        self.secret_layout.addWidget(self.update_button, 0)
        self.secret_layout.addWidget(self.delete_button, 0)
        self.setLayout(self.secret_layout)


    def set_password_visibility(self, checked: bool) -> None:
        if checked:
            self.password_label.setEchoMode(QLineEdit.Normal)
            self.show_button.setIcon(QIcon(os.path.join(os.path.abspath(os.getcwd()), 'src/uis/icons/hide.png')))
        else:
            self.password_label.setEchoMode(QLineEdit.Password)
            self.show_button.setIcon(QIcon(os.path.join(os.path.abspath(os.getcwd()), 'src/uis/icons/show.png')))

    def goto_update_form(self) -> None:
        form = SecretFormView(self, self.stacked_widget, self.master_password, self.secret)
        self.stacked_widget.addWidget(form)
        self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)

    def delete_secret(self) -> None:
        confirm = QMessageBox.question(self, 'Confirm deletion', 'Are you sure you want to delete secret?')
        if confirm == QMessageBox.Yes:
            self.mainWiev.delete_secret_from_list(self.secret)
            delete_secret(self.secret)


    def set_fields(self, secret: Secret) -> None:
        if self.show_button.isChecked():
            self.show_button.click()

        self.secret = secret
        name, login, password, notes = self.secret.get_decrypted_data(self.master_password)
        
        self.id_label.setText(str(self.secret.id))
        self.name_label.setText(name)
        self.login_label.setText(login)
        self.password_label.setText(password)
    