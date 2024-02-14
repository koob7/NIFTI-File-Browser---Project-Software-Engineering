import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMainWindow

from gui_login import GUI_Login
from gui_register import GUI_Register
from gui_window import GUIWindow

class UIMenu(QMainWindow):
    """
    Class UIMenu represents the main menu of the application.

    It allows navigation between the login, registration, and main application screens.
    """

    def __init__(self):
        """
        Initializes the main menu of the application.
        """
        self.app = QtWidgets.QApplication([])

        # Initializing widgets for the login, registration, and main window screens
        login_window_widget = GUI_Login()
        self.main_window_widget = GUIWindow()
        register_window_widget = GUI_Register()

        # Setting the size of the widgets
        self.main_window_widget.resize(800, 600)
        login_window_widget.resize(800, 600)
        register_window_widget.resize(800, 600)

        # Displaying the login screen as the initial screen
        login_window_widget.show()

        # Connecting signals related to navigation between screens
        login_window_widget.main_window.connect(login_window_widget.close)
        login_window_widget.main_window.connect(self.main_window_widget.show)
        login_window_widget.register_window.connect(login_window_widget.close)
        login_window_widget.register_window.connect(register_window_widget.show)
        register_window_widget.main_window.connect(register_window_widget.close)
        register_window_widget.main_window.connect(self.main_window_widget.show)
        register_window_widget.login_window.connect(register_window_widget.close)
        register_window_widget.login_window.connect(login_window_widget.show)

        login_window_widget.close() #do usunięcia przy końcówce projektu!!!
        self.main_window_widget.show() #do usunięcia przy końcówce projektu!!!

        # Running the main application loop
        sys.exit(self.app.exec())
