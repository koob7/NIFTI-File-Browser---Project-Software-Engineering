from PySide6.QtGui import QPixmap, QColor, QPainter, QCursor, QPen
from PySide6.QtWidgets import QLabel
from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtCore import Qt

"""
Nadpisanie klasy FigureCanvasQTAgg w celu przechwytywania wydarzeń
"""


class Canvas(FigureCanvasQTAgg):
    def __init__(self, fig: Figure):
        super(Canvas, self).__init__(fig)
        self.toolbar: NavigationToolbar2QT = None
        self.drawing = False
        self.contour = None

    """
    setToolbar przypisuje jakis toolbar danemu canvasowi od razu go chowając 
    i włączając przesuwanie (nie ma celu bawić się w włączenie tego w wydarzeniach)
    """

    def setToolbar(self, toolbar: NavigationToolbar2QT):
        self.toolbar = toolbar
        self.toolbar.hide()
        self.toolbar.pan()

    """
    Przechwycenie wydarzenia scrollowania - zoom obrazka
    """

    def wheelEvent(self, event):
        ax = self.figure.get_axes()[0]
        ax.use_stick_edges = False
        """^Nie jestem pewny, czy to jest potrzebne"""
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        scale = (xmax - xmin) / (ymax - ymin)
        """angleDelta to różnica w ustawieniu scrolla -> >0 oznacza scrollowanie od siebie ergo przybliżanie"""
        if event.angleDelta().y() > 0:
            ax.set_xlim(xmin + 1.5 * scale, xmax - 1.5 * scale, auto=False)
            ax.set_ylim(ymin + 1.5, ymax - 1.5)
        else:
            ax.set_xlim(xmin - 1.5 * scale, xmax + 1.5 * scale, auto=False)
            ax.set_ylim(ymin - 1.5, ymax + 1.5)
        self.figure.canvas.draw()

    """
    Przechwycenie wydarzenia ruchu, ale tylko jesli rysujemy (przycisk draw dla danego canvasu zostal wcisniety) i trzymamy LPM
    w innym wypadku po prostu odsylamy event do klasy po ktorej dziedziczymy
    """

    def mouseMoveEvent(self, event):
        if self.drawing:
            if event.buttons() and Qt.LeftButton:
                print("drawing")
                # pen = QPen()
                # pen.setWidth(777)
                #
                # painter = QPainter(self)
                # painter.setPen(pen)
                # painter.drawEllipse(15, 15, 200, 200)
                # self.figure.canvas.draw()

        else:
            super(Canvas, self).mouseMoveEvent(event)


    def drawToggle(self):
        if not self.drawing:
            self.drawing = True
        else:
            self.drawing = False
        self.toolbar.pan()
