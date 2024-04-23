import sys

from PyQt5 import uic
from PyQt5.QtWidgets import *
from sympy import latex
from sympy.abc import x as X

from GUI.math_text_label import MathTextLabel
from GUI.plot import MyFuncPlot
from GUI.utils import *
from solve.solver import approximate_func


class UI(QMainWindow):
    x_data = (0, 1, 2, 3, 4, 5, 6, 7)
    y_data = (8, 7, 6, 5, 4, 3, 2, 1)

    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("GUI.ui", self)

        self.findChild(QPushButton, 'solve_btn').clicked.connect(self.gui_input)
        self.findChild(QPushButton, 'load_file_btn').clicked.connect(self.insert_text_from_file)
        self.input_w = self.findChild(QWidget, 'input_widget')
        self.res_w = self.findChild(QWidget, 'res_widget')
        self.input_field = self.findChild(QTextEdit, 'textEdit_input')

        self.res_w.setVisible(False)

        # self._check()

        self.show()

    def insert_text_from_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*)", options=options)
        if fileName:
            try:
                text = open(fileName, 'r').read()
                self.input_field.setText(text)
            except IOError as e:
                show_error(f"File error: {e}")

    def gui_input(self):
        self.solve(self.input_field.toPlainText())

    def solve(self, text):
        self.x_data = list()
        self.y_data = list()
        try:

            for row in text.split('\n'):
                if row == '':
                    continue
                if row.count(' ') > 1:
                    show_error(f'Invalid input format: too many spaces in row {row}')
                    return
                self.x_data.append(float(row.split()[0]))
                self.y_data.append(float(row.split()[1]))

            if len(self.x_data) == 0:
                show_error('Invalid input format: empty file')
                return
        except ValueError:
            show_error('Invalid input format')
            return

        vars = approximate_func(self.x_data, self.y_data)  # s, f, r, pirson

        self.res_w.setVisible(True)
        self.input_w.setVisible(False)
        self.show_graph(*(vars[1:]))

    def show_graph(self, func, s, pirson=None):
        text = 'Data:\n'
        text += '\n'.join([f'{x} {y}' for x, y in zip(self.x_data, self.y_data)])
        self.res_layout = res_layout = self.findChild(QVBoxLayout, 'res_layout')

        clear_layout(self.res_layout)

        self.prop_plot_graph = graph = MyFuncPlot()
        graph.paint_graph([func], [self.x_data, self.y_data])
        res_layout.addWidget(graph)

        text += '\n\nРешение:\n\nFormula:\n'
        # info_layout = QHBoxLayout()
        text += 'f = $' + latex(func) + f'$\n'
        res_layout.addWidget(MathTextLabel('f = $' + latex(func) + f'$'))
        text += f'S={s}\n'
        res_layout.addWidget(MathTextLabel(f'S={s}'))
        if pirson is not None:
            text += f'Пирсон = {pirson}\n'
            res_layout.addWidget(MathTextLabel(f'Пирсон = {pirson}'))

        # res_layout.addLayout(info_layout)

        table = QTableWidget()
        n = len(self.x_data)
        table.setRowCount(n)
        table.setColumnCount(4)

        text += '\nTable\n'
        text += "x_i y_i f(x_i) e_i\n".replace(' ', '\t')
        table.setHorizontalHeaderLabels("x_i y_i f(x_i) e_i".split())

        for i, x, y in zip(range(n), self.x_data, self.y_data):
            phi = func.subs(X, x)  # y+1 # TODO
            table.setItem(i, 0, QTableWidgetItem(str(x)))
            table.setItem(i, 1, QTableWidgetItem(str(y)))
            table.setItem(i, 2, QTableWidgetItem(str(round(phi, 3))))
            table.setItem(i, 3, QTableWidgetItem(str(round(abs(phi - y), 3))))

            text += f'{x}\t{y}\t{round(phi, 3)}\t{round(abs(phi - y), 3)}\n'
        table.setMinimumHeight(300)

        res_layout.addWidget(table)

        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        save_to_file(self, text)

    def _check(self):
        self.show_graph((X - 1) ** 2 + 1, 2)
        clear_layout(self.findChild(QVBoxLayout, 'res_layout'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UI()
    app.exec_()
