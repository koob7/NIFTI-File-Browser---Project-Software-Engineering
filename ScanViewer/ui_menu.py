import sys
#
from PySide6 import QtWidgets
from PySide6.QtGui import QPixmap, QColor, QPainter
from PySide6.QtWidgets import QLabel, QMainWindow

from gui_login import GUI_Login
from gui_register import GUI_Register
from gui_window import GUIWindow


class UIMenu(QMainWindow):
    def __init__(self):
        app = QtWidgets.QApplication([])
        menu = 0
        login_window_widget = GUI_Login()
        main_window_widget = GUIWindow()
        register_window_widget = GUI_Register()
        main_window_widget.resize(800, 600)
        login_window_widget.resize(800, 600)
        register_window_widget.resize(800, 600)


        login_window_widget.show()
        login_window_widget.main_window.connect(login_window_widget.close)
        login_window_widget.main_window.connect(main_window_widget.show)
        login_window_widget.register_window.connect(login_window_widget.close)
        login_window_widget.register_window.connect(register_window_widget.show)
        register_window_widget.main_window.connect(register_window_widget.close)
        register_window_widget.main_window.connect(main_window_widget.show)
        register_window_widget.login_window.connect(register_window_widget.close)
        register_window_widget.login_window.connect(login_window_widget.show)


        sys.exit(app.exec())
