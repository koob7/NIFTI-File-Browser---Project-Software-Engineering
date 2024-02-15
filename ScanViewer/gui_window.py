from PySide6 import QtCore, QtWidgets
from status import LoginStatus
from filedialogs import open_file_dialog
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT
from matplotlib.figure import Figure
import nibabel
import os
from canvas import Canvas
from contour import Contour
from annotation import ContourAnnotation, Annotation
from storage import Storage


class GUIWindow(QtWidgets.QWidget):
    """
    Class GUIWindow represents the main window of the application.

    It sets up the GUI and handles all the application's functionalities.
    """

    def __init__(self):
        """Initializes the class, setting up all the elements of the GUI and how they are laid out in the window"""
        super().__init__()
        self.profession = LoginStatus.read_profession()
        self.contourList: [Contour] = None
        self.annotation: Annotation = None
        self.img = None
        self.fig_left = Figure(figsize=(8, 6))
        self.fig_mid = Figure(figsize=(8, 6))
        self.fig_right = Figure(figsize=(8, 8))
        self.nii_name = ""

        """Initialization of buttons used in the app"""
        self.load = QtWidgets.QPushButton("Load Image")
        self.reset_left = QtWidgets.QPushButton('Reset')
        self.reset_mid = QtWidgets.QPushButton('Reset')
        self.reset_right = QtWidgets.QPushButton('Reset')
        self.draw_left = QtWidgets.QPushButton('Draw')
        self.draw_mid = QtWidgets.QPushButton('Draw')
        self.draw_right = QtWidgets.QPushButton('Draw')

        """Initialization of text areas representing the annotations made in the app"""
        self.text_left = QtWidgets.QTextEdit()
        self.text_mid = QtWidgets.QTextEdit()
        self.text_right = QtWidgets.QTextEdit()
        self.text_general = QtWidgets.QTextEdit()
        self.text_general.textChanged.connect(lambda: self.annotation.set_annotation(self.text_general.toPlainText()))

        """Initialization of Canvases displaying the scans"""
        self.canvas_left = Canvas(self.fig_left)
        self.canvas_mid = Canvas(self.fig_mid)
        self.canvas_right = Canvas(self.fig_right)
        self.toolbar_left = NavigationToolbar2QT(self.canvas_left, self)
        self.canvas_left.set_toolbar(self.toolbar_left)
        self.toolbar_mid = NavigationToolbar2QT(self.canvas_mid, self)
        self.canvas_mid.set_toolbar(self.toolbar_mid)
        self.toolbar_right = NavigationToolbar2QT(self.canvas_right, self)
        self.canvas_right.set_toolbar(self.toolbar_right)

        """Initialization of sliders allowing for changing the scan's layer"""
        self.slider1 = QtWidgets.QSlider()
        self.slider1.setMinimum(0)
        self.slider1.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider1.valueChanged.connect(lambda: self.slide_plot(self.canvas_left, "left"))
        self.slider2 = QtWidgets.QSlider()
        self.slider2.setMinimum(0)
        self.slider2.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider2.valueChanged.connect(lambda: self.slide_plot(self.canvas_mid, "mid"))
        self.slider3 = QtWidgets.QSlider()
        self.slider3.setMinimum(0)
        self.slider3.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider3.valueChanged.connect(lambda: self.slide_plot(self.canvas_right, "right"))

        """Setting up the layout of the app"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.buttons = QtWidgets.QHBoxLayout(self)
        self.buttons_left = QtWidgets.QHBoxLayout(self)
        self.buttons_left.addWidget(self.reset_left)
        if self.profession == LoginStatus.Profession.ADMIN or LoginStatus.profession.PHYSICIAN:
            self.buttons_left.addWidget(self.draw_left)
        if self.profession != LoginStatus.Profession.ADMIN and LoginStatus.profession.DOCTOR:
            self.text_left.setDisabled(True)
        self.buttons.addLayout(self.buttons_left)
        self.buttons_mid = QtWidgets.QHBoxLayout(self)
        self.buttons_mid.addWidget(self.reset_mid)
        if self.profession == LoginStatus.Profession.ADMIN or LoginStatus.profession.PHYSICIAN:
            self.buttons_mid.addWidget(self.draw_mid)
        if self.profession != LoginStatus.Profession.ADMIN and LoginStatus.profession.DOCTOR:
            self.text_mid.setDisabled(True)
        self.buttons.addLayout(self.buttons_mid)
        self.buttons_right = QtWidgets.QHBoxLayout(self)
        self.buttons_right.addWidget(self.reset_right)
        if self.profession == LoginStatus.Profession.ADMIN or LoginStatus.profession.PHYSICIAN:
            self.buttons_right.addWidget(self.draw_right)
        if self.profession != LoginStatus.Profession.ADMIN and LoginStatus.profession.DOCTOR:
            self.text_right.setDisabled(True)
        self.buttons.addLayout(self.buttons_right)
        canvas_layout = QtWidgets.QHBoxLayout(self)
        canvas_layout.addWidget(self.canvas_left)
        canvas_layout.addWidget(self.canvas_mid)
        canvas_layout.addWidget(self.canvas_right)
        slider_layout = QtWidgets.QHBoxLayout(self)
        slider_layout.addWidget(self.slider1)
        slider_layout.addWidget(self.slider2)
        slider_layout.addWidget(self.slider3)
        contour_annotation_layout = QtWidgets.QHBoxLayout(self)
        contour_annotation_layout.addWidget(self.text_left)
        contour_annotation_layout.addWidget(self.text_mid)
        contour_annotation_layout.addWidget(self.text_right)
        self.layout.addWidget(self.load)
        self.layout.addLayout(self.buttons)
        self.layout.addLayout(canvas_layout)
        self.layout.addLayout(slider_layout)
        self.layout.addLayout(contour_annotation_layout)
        self.layout.addWidget(self.text_general)
        if self.profession != LoginStatus.Profession.ADMIN and LoginStatus.profession.DOCTOR:
            self.text_general.setDisabled(True)

        """Button connections"""
        self.load.clicked.connect(self.load_scan)
        self.reset_left.clicked.connect(self.toolbar_left.home)
        self.reset_mid.clicked.connect(self.toolbar_mid.home)
        self.reset_right.clicked.connect(self.toolbar_right.home)
        self.draw_left.clicked.connect(self.canvas_left.draw_toggle)
        self.draw_mid.clicked.connect(self.canvas_mid.draw_toggle)
        self.draw_right.clicked.connect(self.canvas_right.draw_toggle)

    @QtCore.Slot()
    def draw_plots(self, fig: Figure, panel):
        """
        Function used to draw the chosen layer of the scan onto the Canvases
        This function is freely available in the niBabel library documentation
        """
        if len(fig.axes) != 0:
            ax = fig.get_axes()[0]
            ax.set_axis_off()
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
        """
        This function handles loading the scan for the first time after using the Load Image button
        """
        """ This part handles closing and saving the previous image had it been loaded before"""
        if self.nii_name != "":
            Storage.serialize(self.nii_name+".pickle", self.annotation, self.contourList)

            self.fig_left.clear()
            self.fig_mid.clear()
            self.fig_right.clear()
            self.img = None

        """This part handles loading the data from the chosen file into variables"""
        filepath = open_file_dialog()
        if filepath is None:
            QtWidgets.QMessageBox.warning(self, "Loading Failed", "Please choose file.")
            return
        wrapped_img = nibabel.load(filepath)
        self.nii_name = os.path.splitext(os.path.basename(filepath))[0]
        """
        This part checks if this scan has been loaded before and if so,
         loads the contours and annotations made last time
         """
        self.annotation, self.contourList = Storage.deserialize(self.nii_name+".pickle")
        if self.annotation is None:
            self.annotation = Annotation()
        if self.contourList is None:
            self.contourList = []
        """This part parses the loaded data into plots and draws them on their respective Canvases"""
        self.img = wrapped_img.get_fdata()
        self.text_general.setText(self.annotation.annotation)
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

    def slide_plot(self, canvas: Canvas, panel):
        """
        This function handles everything that happens after a slider is moved.

        After a slider is moved, the canvas has to make sure the contour and annotation made on its previous layer
        are properly saved and then needs to display the new layer whilst checking if there are already preexisting
        contours and annotation made for the new layer - if there are they have to be loaded, if there aren't new
        instances of those objects have to be created.
        :param canvas: Canvas to draw on
        :param panel: Which panel (left, middle or right) is the canvas on
        :return: None
        """
        if self.img is None:
            return
        if panel == "left":
            if canvas.annotation is not None:
                canvas.annotation.annotation = self.text_left.toPlainText()
        elif panel == "mid":
            if canvas.annotation is not None:
                canvas.annotation.annotation = self.text_mid.toPlainText()
        elif panel == "right":
            if canvas.annotation is not None:
                canvas.annotation.annotation = self.text_right.toPlainText()
        canvas.clear_contour()
        self.draw_plots(canvas.figure, panel)
        layer = 0
        found_new = False
        if panel == "left":
            layer = self.slider1.value()
            self.text_left.clear()
        elif panel == "mid":
            layer = self.slider2.value()
            self.text_mid.clear()
        elif panel == "right":
            layer = self.slider3.value()
            self.text_right.clear()
        for annotation in self.annotation.contourAnnotations:
            if annotation.layer == layer and annotation.panel == panel:
                canvas.annotation = annotation
                found_new = True
                if panel == "left":
                    self.text_left.setText(annotation.annotation)
                elif panel == "mid":
                    self.text_mid.setText(annotation.annotation)
                elif panel == "right":
                    self.text_right.setText(annotation.annotation)
        if not found_new:
            new_annotation = ContourAnnotation(panel, layer)
            canvas.annotation = new_annotation
        found_new = False
        for contour in self.contourList:
            if contour.layer == layer and contour.panel == panel:
                canvas.contour = contour
                canvas.redraw_contour()
                found_new = True
        if not found_new:
            new_contour = Contour(panel, layer)
            self.annotation.contourAnnotations.append(new_annotation)
            self.contourList.append(new_contour)
            canvas.contour = new_contour

    def __del__(self):
        """Destructor of the class, saves the contours and annotations if the user leaves."""
        if self.nii_name != "":
            Storage.serialize(self.nii_name+".pickle", self.annotation, self.contourList)
