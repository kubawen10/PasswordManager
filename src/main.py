import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from utils.ui_utils import get_ui_file, get_icon_file

from models.utils import create_db
from views.login_view import LoginView

if __name__ == '__main__':
    create_db()
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()
    login = LoginView(stacked_widget)
    stacked_widget.addWidget(login)
    stacked_widget.setFixedWidth(1200)
    stacked_widget.setFixedHeight(800)
    stacked_widget.show()
    app.exec()


