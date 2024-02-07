import sys

from PySide6 import QtWidgets
from PySide6.QtGui import QPixmap, QColor, QPainter
from PySide6.QtWidgets import QLabel, QMainWindow

from gui_window import GUIWindow

class UIMenu(QMainWindow):
    def __init__(self):
        app = QtWidgets.QApplication([])


        widget = GUIWindow()
        widget.resize(800, 600)
        widget.show()

        sys.exit(app.exec())
