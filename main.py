# I am author!
import sys
import math
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import QPoint
# import numpy as np

SCREEN_SIZE = [500, 500]
# a list of tuples, each representing the sequence of opening files
TYPE = [(1, 2, 3), (1, 2, 3, 4), (1, 2, 3, 4, 5), (1, 2, 3, 4, 5), (1, 2, 3, 4),
        (1, 2, 3, 4, 43), (1, 2, 3, 4, 41), (1, 2, 3, 4, 41), (1, 2, 3, 4, 41, 42),
        (1, 2, 3, 4,), ()]
INFORMATION = []
POINTS = {}


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('test.ui', self)
        # Загружаем дизайн
        self.initUI()

    def initUI(self):
        pass

    def paintEvent(self, event):
        # Создаем объект QPainter для рисования
        qp = QPainter()
        # Начинаем процесс рисования
        qp.begin(self)
        self.draw_flag(qp)
        # Завершаем рисование
        qp.end()

    def draw_flag(self, qp):
        pass

    def information(self):
        pass

    def t_event(self):
        pass

    def add_param(self, state):
        pass


def xs(self,x):
    return x + SCREEN_SIZE[0] // 2


def ys(self,y):
    return SCREEN_SIZE[1] // 2 - y


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
