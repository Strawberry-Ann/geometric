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
        (1, 2, 3, 4, 7), (1, 2, 3, 4, 41), (1, 2, 3, 4, 41), (1, 2, 3, 4, 41, 42),
        (1, 2, 3, 4,), ()]
FUNCTIONS = {'1': [lambda x: x.split()],
             '2': [lambda x: x.split()],
             '3': [lambda x: list(map(lambda y: (y.split('-')[0], y.split('-')[1]), x.split())),
                   lambda x: list(map(lambda y: (y.split('=')[0].split(':'), y.split('=')[1].split(':')), x.split()))],
             '4': [lambda x: list(map(lambda y: (y.split('-')[0], y.split('-')[1]), x.split())),
                   lambda x: list(map(lambda y: (y.split('=')[0].split(':'), y.split('=')[1].split(':')), x.split()))],
             '5': [lambda name: name, lambda heights: heights.split(), lambda medians: medians.split(),
                   lambda simedians: simedians.split(), lambda cevians: cevians],
             '6': [lambda text: list(map(lambda string: string.split(), text.split('\n')))],
             '7': [lambda name1: name1, lambda value1: value1, lambda name2: name2, lambda value2: value2,
                   lambda string: list(map(lambda x: (x.split('=')[1], x.split('=')[0].split('*')[0],
                                                      x.split('=')[0].split('*')[1]), string.split()))],
             '8': [lambda string: list(map(lambda x: (x.split('=')[1], x.split('=')[0].split('*')[0],
                                                      x.split('=')[0].split('*')[1]), string.split()))]}
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
