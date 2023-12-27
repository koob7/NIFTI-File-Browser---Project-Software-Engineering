import os.path

import sys
import random
import nibabel
import numpy as np
from matplotlib.figure import Figure
from PySide6 import QtCore, QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from filedialogs import open_file_dialog
from nibabel.testing import data_path


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.img = None

        self.fig_left = Figure()
        self.fig_mid = Figure()
        self.fig_right = Figure()

        self.canvas_left = FigureCanvasQTAgg(self.fig_left)
        self.canvas_mid = FigureCanvasQTAgg(self.fig_mid)
        self.canvas_right = FigureCanvasQTAgg(self.fig_right)

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
        canvas_layout = QtWidgets.QHBoxLayout(self)
        canvas_layout.addWidget(self.canvas_left)
        canvas_layout.addWidget(self.canvas_mid)
        canvas_layout.addWidget(self.canvas_right)
        slider_layout = QtWidgets.QHBoxLayout(self)
        slider_layout.addWidget(self.slider1)
        slider_layout.addWidget(self.slider2)
        slider_layout.addWidget(self.slider3)
        self.layout.addWidget(self.load)
        self.layout.addLayout(canvas_layout)
        self.layout.addLayout(slider_layout)

        self.load.clicked.connect(self.load_scan)

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
