# I am author!
import sys
import math
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import QPoint
# import numpy as np

SCREEN_SIZE = [500, 500]
INFORMATION = []


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
        self.add_param(self.name_t)
        self.type_seg.buttonClicked.connect(self.add_param)
        self.type_cor.buttonClicked.connect(self.add_param)
        self.inf_t.setText(*self.triangle)

    def add_param(self, state):
        self.triangle.append(state.text())


class Point(QPoint):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def draw(self, qp):
        qp.drawPoint(self, self.x, self.y)


class Straight:
    def __init__(self, name, p1, p2):
        self.name = name
        self.p1 = p1
        self.p2 = p2

    def draw(self, qp):
        qp.drawLine(self.p1, self.p2)


class LineSegment:
    def __init__(self, name, p1, p2):
        self.name = name
        self.p1 = p1
        self.p2 = p2

    def draw(self, qp):
        qp.drawLine(self.p1, self.p2)


class Ray:
    def __init__(self, name, p1, p2):
        self.name = name
        self.p1, self.p2 = p1, p2

    def draw(self, qp):
        qp.drawLine(self.p1, self.p2)


class Corner:
    def __init__(self, p1, p2, size):
        self.p1 = p1
        self.p2 = p2
        self.size = size

    def draw(self, qp):
        qp.drawPoint(self.p1)
        qp.drawLine(self.p1, self.p2)
        qp.drawLine(self.p1, Point(self.p2.x))


class Triangle:
    def __init__(self, p1='A', p2='B', p3='C',
                 s1=1, s2=1, s3=1, c1=60, c2=60, c3=60):
        self.p1, self.p2, self.p3 = p1, p2, p3
        self.s1, self.s2, self.s3 = s1, s2, s3
        self.c1, self.c2, self.c3 = c1, c2, c3


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
