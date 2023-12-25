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
        self.fig = Figure()

        self.load = QtWidgets.QPushButton("Load Image")
        self.slider1 = QtWidgets.QSlider()
        self.slider1.setMinimum(0)
        self.slider1.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider1.valueChanged.connect(self.draw_plots)
        self.slider1.setTracking(False)
        self.slider2 = QtWidgets.QSlider()
        self.slider2.setMinimum(0)
        self.slider2.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider2.valueChanged.connect(self.draw_plots)
        self.slider2.setTracking(False)
        self.slider3 = QtWidgets.QSlider()
        self.slider3.setMinimum(0)
        self.slider3.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider3.valueChanged.connect(self.draw_plots)
        self.slider3.setTracking(False)
        self.static_canvas = FigureCanvasQTAgg(self.fig)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.load)
        self.layout.addWidget(NavigationToolbar2QT(self.static_canvas, self))
        self.layout.addWidget(self.static_canvas)
        self.layout.addWidget(self.slider1)
        self.layout.addWidget(self.slider2)
        self.layout.addWidget(self.slider3)

        self.load.clicked.connect(self.load_scan)

    @QtCore.Slot()
    def draw_plots(self):
        img_data = self.img.get_fdata()
        ax1 = self.fig.add_subplot(1, 3, 1)
        ax2 = self.fig.add_subplot(1, 3, 2)
        ax3 = self.fig.add_subplot(1, 3, 3)
        axs = [ax1, ax2, ax3]
        slice_0 = img_data[self.slider1.value(), :, :, 0]
        slice_1 = img_data[:, self.slider2.value(), :, 0]
        slice_2 = img_data[:, :, self.slider3.value(), 0]
        slices = [slice_0, slice_1, slice_2]
        for i, slice in enumerate(slices):
            axs[i].imshow(slice.T, cmap="gray", origin="lower")
        self.static_canvas.draw()
        "updating all plots when only 1 perspective is changed is inefficient - split it, maybe plausible to reenable tracking"
    @QtCore.Slot()
    def load_scan(self):
        filepath = open_file_dialog()
        self.img = nibabel.load(filepath)
        self.slider1.setValue(int(self.img.shape[0]/2))
        self.slider2.setValue(int(self.img.shape[1]/2))
        self.slider3.setValue(int(self.img.shape[2]/2))
        self.slider1.setMaximum(self.img.shape[0])
        self.slider2.setMaximum(self.img.shape[1])
        self.slider3.setMaximum(self.img.shape[2])
        self.draw_plots()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
