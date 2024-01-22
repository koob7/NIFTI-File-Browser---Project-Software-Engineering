import os.path

import sys
import random
import nibabel
import numpy as np
from PySide6.QtCore import Qt
from matplotlib.figure import Figure
from PySide6 import QtCore, QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from filedialogs import open_file_dialog
from nibabel.testing import data_path


class Canvas(FigureCanvasQTAgg):
    def __init__(self, fig: Figure):
        super(Canvas, self).__init__(fig)
        self.toolbar: NavigationToolbar2QT = None
        self.drawing = False
        self.contour = None

    def setToolbar(self, toolbar: NavigationToolbar2QT):
        self.toolbar = toolbar
        self.toolbar.hide()
        self.toolbar.pan()

    def wheelEvent(self, event):
        ax = self.figure.get_axes()[0]
        ax.use_stick_edges = False
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        scale = (xmax - xmin) / (ymax - ymin)
        if event.angleDelta().y() > 0:
            ax.set_xlim(xmin+1.5 * scale, xmax-1.5 * scale, auto=False)
            ax.set_ylim(ymin+1.5, ymax-1.5)
        else:
            ax.set_xlim(xmin - 1.5 * scale, xmax + 1.5 * scale, auto=False)
            ax.set_ylim(ymin - 1.5, ymax + 1.5)
        self.figure.canvas.draw()

    def mouseMoveEvent(self, event):
        if self.drawing:
            if event.buttons() and Qt.LeftButton:
                print("drawing")
        else:
            super(Canvas, self).mouseMoveEvent(event)

    def drawToggle(self):
        if not self.drawing:
            self.drawing = True
        else:
            self.drawing = False
        self.toolbar.pan()

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.img = None
        self.fig_left = Figure(figsize=(8, 6))
        self.fig_mid = Figure(figsize=(8, 6))
        self.fig_right = Figure(figsize=(8, 8))

        self.reset_left = QtWidgets.QPushButton('Reset')
        self.reset_mid = QtWidgets.QPushButton('Reset')
        self.reset_right = QtWidgets.QPushButton('Reset')
        self.draw_left = QtWidgets.QPushButton('Draw')
        self.draw_mid = QtWidgets.QPushButton('Draw')
        self.draw_right = QtWidgets.QPushButton('Draw')

        self.canvas_left = Canvas(self.fig_left)
        self.canvas_mid = Canvas(self.fig_mid)
        self.canvas_right = Canvas(self.fig_right)
        self.toolbar_left = NavigationToolbar2QT(self.canvas_left, self)
        self.canvas_left.setToolbar(self.toolbar_left)
        self.toolbar_mid = NavigationToolbar2QT(self.canvas_mid, self)
        self.canvas_mid.setToolbar(self.toolbar_mid)
        self.toolbar_right = NavigationToolbar2QT(self.canvas_right, self)
        self.canvas_right.setToolbar(self.toolbar_right)
        self.load = QtWidgets.QPushButton("Load Image")
        self.slider1 = QtWidgets.QSlider()
        self.slider1.setMinimum(0)
        self.slider1.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider1.valueChanged.connect(lambda: self.draw_plots(self.fig_left, "left"))
        self.slider2 = QtWidgets.QSlider()
        self.slider2.setMinimum(0)
        self.slider2.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider2.valueChanged.connect(lambda: self.draw_plots(self.fig_mid, "mid"))
        self.slider3 = QtWidgets.QSlider()
        self.slider3.setMinimum(0)
        self.slider3.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider3.valueChanged.connect(lambda: self.draw_plots(self.fig_right, "right"))

        self.layout = QtWidgets.QVBoxLayout(self)
        self.buttons = QtWidgets.QHBoxLayout(self)
        self.buttons_left = QtWidgets.QHBoxLayout(self)
        self.buttons_left.addWidget(self.reset_left)
        self.buttons_left.addWidget(self.draw_left)
        self.buttons.addLayout(self.buttons_left)
        self.buttons_mid = QtWidgets.QHBoxLayout(self)
        self.buttons_mid.addWidget(self.reset_mid)
        self.buttons_mid.addWidget(self.draw_mid)
        self.buttons.addLayout(self.buttons_mid)
        self.buttons_right = QtWidgets.QHBoxLayout(self)
        self.buttons_right.addWidget(self.reset_right)
        self.buttons_right.addWidget(self.draw_right)
        self.buttons.addLayout(self.buttons_right)
        canvas_layout = QtWidgets.QHBoxLayout(self)
        canvas_layout.addWidget(self.canvas_left)
        canvas_layout.addWidget(self.canvas_mid)
        canvas_layout.addWidget(self.canvas_right)
        slider_layout = QtWidgets.QHBoxLayout(self)
        slider_layout.addWidget(self.slider1)
        slider_layout.addWidget(self.slider2)
        slider_layout.addWidget(self.slider3)
        self.layout.addWidget(self.load)
        self.layout.addLayout(self.buttons)
        self.layout.addLayout(canvas_layout)
        self.layout.addLayout(slider_layout)

        self.load.clicked.connect(self.load_scan)
        self.reset_left.clicked.connect(self.toolbar_left.home)
        self.reset_mid.clicked.connect(self.toolbar_mid.home)
        self.reset_right.clicked.connect(self.toolbar_right.home)
        self.draw_left.clicked.connect(self.canvas_left.drawToggle)

    @QtCore.Slot()
    def draw_plots(self, fig: Figure, panel):
        if len(fig.axes) != 0:
            ax = fig.get_axes()[0]
            slice = None
            if panel == "left":
                slice = self.img[self.slider1.value(), :, :, 0]
            elif panel == "mid":
                slice = self.img[:, self.slider2.value(), :, 0]
            elif panel == "right":
                slice = self.img[:, :, self.slider3.value(), 0]
            ax.imshow(slice.T, cmap="gray", origin="lower")
            fig.canvas.draw()

    @QtCore.Slot()
    def load_scan(self):
        filepath = open_file_dialog()
        wrapped_img = nibabel.load(filepath)
        self.img = wrapped_img.get_fdata()
        self.fig_left.add_subplot(111)
        self.fig_mid.add_subplot(111)
        self.fig_right.add_subplot(111)
        self.slider1.setValue(int(self.img.shape[0] / 2))
        self.slider2.setValue(int(self.img.shape[1] / 2))
        self.slider3.setValue(int(self.img.shape[2] / 2))
        self.slider1.setMaximum(self.img.shape[0]-1)
        self.slider2.setMaximum(self.img.shape[1]-1)
        self.slider3.setMaximum(self.img.shape[2]-1)
        self.draw_plots(self.fig_left, "left")
        self.draw_plots(self.fig_mid, "mid")
        self.draw_plots(self.fig_right, "right")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
