from PyQt5.QtWidgets import QDialog, QStackedWidget, QListWidget, QPushButton, QHBoxLayout, QLabel, QVBoxLayout, QListWidgetItem, QWidget, QLineEdit, QMessageBox

from models.secret import Secret, get_all_secrets, delete_secret
from .secret_form_view import SecretFormView


class MainView(QDialog):
    def __init__(self, stacked_widget: QStackedWidget, master_password: str) -> None:
        super(MainView, self).__init__()
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

    def add_secret_to_list(self, secret: Secret) -> None:
        secret_widget = SecretWidget(self.list_widget, self, self.stacked_widget, secret, self.master_password)
        list_item = QListWidgetItem(self.list_widget)
        list_item.setSizeHint(secret_widget.sizeHint())
        self.list_widget.addItem(list_item)
        self.list_widget.setItemWidget(list_item, secret_widget)

    def delete_secret_from_list(self, secret: Secret) -> None:
        for index in range(self.list_widget.count()):
            item = self.list_widget.item(index)
            cur_secret = self.list_widget.itemWidget(item).secret

            if cur_secret.id == secret.id:
                self.list_widget.takeItem(index)
                break

    def goto_add_secret_form(self) -> None:
        form = SecretFormView(self, self.stacked_widget, self.master_password)
        self.stacked_widget.addWidget(form)
        self.stacked_widget.setCurrentIndex(self.stacked_widget.currentIndex() + 1)


class SecretWidget(QWidget):
    def __init__(self, parent: QListWidget, mainWiev: MainView, stacked_widget: QStackedWidget, secret: Secret, master_password: str):
        super(SecretWidget, self).__init__(parent)
        self.setStyleSheet('color: white')
        
        self.mainWiev = mainWiev
        self.stacked_widget = stacked_widget
        self.master_password = master_password

        self.id_label = QLabel()
        self.name_label = QLabel()
        self.login_label = QLineEdit()
        self.password_label = QLineEdit()

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

        self.delete_button = QPushButton('delete')
        self.delete_button.clicked.connect(self.delete_secret)

        self.set_fields(secret)
        
        self.secret_layout = QHBoxLayout()
        self.secret_layout.addWidget(self.id_label,0)
        self.secret_layout.addWidget(self.name_label,1)
        self.secret_layout.addWidget(self.login_label,1)
        self.secret_layout.addWidget(self.password_label,1)
        self.secret_layout.addWidget(self.show_button, 0)
        self.secret_layout.addWidget(self.update_button, 0)
        self.secret_layout.addWidget(self.delete_button, 0)
        self.setLayout(self.secret_layout)

    def set_password_visibility(self, checked: bool) -> None:
        if checked:
            self.password_label.setEchoMode(QLineEdit.Normal)
        else:
            self.password_label.setEchoMode(QLineEdit.Password)

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
    