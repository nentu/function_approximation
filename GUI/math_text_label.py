from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MathTextLabel(QtWidgets.QWidget):

    def __init__(self, mathText, parent=None, **kwargs):
        super(QtWidgets.QWidget, self).__init__(parent, **kwargs)

        l = QVBoxLayout(self)
        l.setContentsMargins(0, 0, 0, 0)

        r, g, b, a = self.palette().base().color().getRgbF()

        self._figure = Figure(edgecolor=(r, g, b), facecolor=(r, g, b))
        self._canvas = FigureCanvas(self._figure)
        l.addWidget(self._canvas)
        self._figure.clear()
        text = self._figure.suptitle(
            mathText,
            x=0.0,
            y=0.75,
            horizontalalignment='left',
            verticalalignment='top',
            size=QtGui.QFont().pointSize() * 2
        )
        self._canvas.draw()

        (x0, y0), (x1, y1) = text.get_window_extent().get_points()
        w = x1 - x0
        h = y1 - y0
        h *= 2

        self._figure.set_size_inches(w / 80, h / 80)
        self.setFixedSize(int(w), int(h))
