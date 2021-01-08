# Структура проекта


import sys
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from math import sin, cos, asin, pi, sqrt
from random import choice, sample
from sympy.geometry import *
from PyQt5 import uic
from PyQt5.QtCore import Qt


SCREEN_SIZE = [500, 500]
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
POINTS = {}
FIGURES = list()



class Work(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)
        self.initUI()
        self.t = True

    def initUI(self):
        self.g = [self.add_altitude, self.add_bisector, self.add_circumcircle,
                               self.add_eulerline, self.add_incircle, self.add_medial,
                               self.add_median, self.add_ninepointcircle]
        self.bgf.buttonClicked.connect(self.clckd)

    @QtCore.pyqtSlot()
    def gif_display(self):
        l = QMovieLabel('loading.gif', self)
        l.adjustSize()
        l.show()

    def clckd(self, btn):
        if btn == self.add_altitude or btn == self.add_bisector or btn == self.add_median:
            point, ok_pressed = QInputDialog.getItem(
                self, "Выберите вершину", "Из какой вершины нужно провести чевиану?",
                ("A", "B", "C"), 1, False)

        else:
            for tr in TRIANGLES:
                FIGURES.append(tr.BUTTON_FUNCTIONS[self.g.index(btn)])


class Drawing(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 900, 900)
        self.setWindowTitle('Рисование')
        for tr in TRIANGLES:
            FIGURES.append(tr.add_ninepointcircle())
            FIGURES.append(tr.add_incircle())

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_flag(qp)
        qp.end()

    def draw_flag(self, qp):
        for f in FIGURES:
            f.draw(qp)
        for tr in TRIANGLES:
            tr.draw(qp)



class GroupFigures:
    pass


class MyPoint(Point2D):
    def draw(self, qp):
        # нарисуем точку в виде пустого круга с толщиной линии 1
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        qp.setPen(pen)
        color = QColor(255, 255, 255)
        qp.setBrush(color)
        qp.drawEllipse(int(self.x - 2), int(self.y - 2), 4, 4)


class MyLineSegment(Segment2D):
    def draw(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(int(self.p1.x), int(self.p1.y),
                    int(self.p2.x), int(self.p2.y))
        pen.setStyle(Qt.DotLine)
        qp.setPen(pen)
        self.p1.draw(qp)
        self.p2.draw(qp)


class MyStraight(Line2D):
    def draw(self, qp):
        pen = QPen(Qt.black, 2, Qt.DotLine)
        qp.setPen(pen)
        dx, dy = abs(self.p1.x - self.p2.x) // 2,\
                 abs(self.p1.y - self.p2.y) // 2
        x1, y1, x2, y2 = self.p1.x, self.p1.y, self.p2.x, self.p2.y
        if x1 >= x2 and y1 >= y2:
            qp.drawLine(x1 + dx, y1 + dy, x2 - dx, y2 - dy)
        elif x1 <= x2 and y1 <= y2:
            qp.drawLine(x1 - dx, y1 - dy, x2 + dx, y2 + dy)
        elif x1 <= x2 and y1 >= y2:
            qp.drawLine(x1 - dx, y1 + dy, x2 + dx, y2 - dy)
        elif x1 >= x2 and y1 <= y2:
            qp.drawLine(x1 + dx, y1 - dy, x2 - dx, y2 + dy)
        MyLineSegment(self.p1, self.p2).draw(qp)


class MyRay(Ray2D):
    def draw(self, qp):
        pen = QPen(Qt.black, 2, Qt.DotLine)
        qp.setPen(pen)
        dx, dy = int(abs(self.p1.x - self.p2.x) // 2), int(abs(self.p1.y - self.p2.y) // 2)
        x1, y1, x2, y2 = int(self.p1.x), int(self.p1.y), int(self.p2.x), int(self.p2.y)
        if x1 >= x2 and y1 >= y2:
            qp.drawLine(x1, y1, x2 - dx, y2 - dy)
        elif x1 <= x2 and y1 <= y2:
            qp.drawLine(x1, y1, x2 + dx, y2 + dy)
        elif x1 <= x2 and y1 >= y2:
            qp.drawLine(x1, y1, x2 + dx, y2 - dy)
        elif x1 >= x2 and y1 <= y2:
            qp.drawLine(x1, y1, x2 - dx, y2 + dy)
        MyLineSegment(self.p1, self.p2).draw(qp)


class MyCircle(Circle):
    def __init__(self, center, radius):
        Circle.__init__(center, radius, radius)

    def draw(self, qp):
        pen = QPen(Qt.black, 2, Qt.DotLine)
        qp.setPen(pen)
        r = self.hradius
        qp.drawEllipse(self.center.coordinates[0] - r, self.center.coordinates[1] - r, self.hradius * 2, self.vradius * 2)
        self.center.draw(qp)


# класс угла, который является частью замкнутой фигуры на плоскости
class MyCorner:
    def __init__(self, size, p1, p2, line=None):
        self.p1 = p1
        self.p2 = p2
        self.s = size
        self.init_p3(line)

    def init_p3(self, line):
        global m
        # plotting p3 of a given value using the math library
        if line == None:
            line = sqrt((self.p2.x - self.p1.x) ** 2 + (self.p2.y - self.p1.y) ** 2)
        else:
            line = line
        if self.p1.x <= self.p2.x and self.p1.y < self.p2.y:
            m = [self.p1.x + line * sin(self.s * pi / 180 + asin((self.p2.x - self.p1.x) / line)),
                 line * cos(self.s * pi / 180 + asin((self.p2.x - self.p1.x) / line)) + self.p1.y]
        elif self.p1.y <= self.p2.y and self.p1.x > self.p2.x:
            m = [self.p1.x - line * cos(self.s * pi / 180 + asin((self.p2.y - self.p1.y) / line)),
                 line * sin(self.s * pi / 180 + asin((self.p2.y - self.p1.y) / line)) + self.p1.y]
        elif self.p1.x >= self.p2.x and self.p1.y > self.p2.y:
            m = [self.p1.x - line * sin(self.s * pi / 180 + asin((self.p2.x - self.p1.x) / line)),
                 -line * cos(self.s * pi / 180 + asin((self.p1.x - self.p2.x) / line)) + self.p1.y]
        elif self.p1.y >= self.p2.y and self.p1.x < self.p2.x:
            m = [self.p1.x + line * cos(self.s * pi / 180 + asin((self.p1.y - self.p2.y) / line)),
                 -line * sin(self.s * pi / 180 + asin((self.p1.y - self.p2.y) / line)) + self.p1.y]
        self.p3 = MyPoint(m[0], m[1])

    def draw(self, qp):
        MyLineSegment(self.p1, self.p2).draw(qp)
        MyLineSegment(self.p1, self.p3).draw(qp)


class MyTriangle(Triangle):
    def __init__(self, *args):
        super().__init__()
        self.BUTTON_FUNCTIONS = [self.add_altitude, self.add_bisector, self.add_circumcircle,
                               self.add_eulerline, self.add_incircle, self.add_medial,
                               self.add_median, self.add_ninepointcircle]

    def draw(self, qp):
        p1, p2, p3 = self.vertices[0], self.vertices[1], self.vertices[2]
        MyLineSegment(p1, p2).draw(qp)
        MyLineSegment(p2, p3).draw(qp)
        MyLineSegment(p3, p1).draw(qp)

    def add_median(self, p):
        ms = self.medians[p]
        return MyLineSegment(ms.p1, MyPoint(ms.p2.x, ms.p2.y))

    def add_bisector(self, p):
        bs = self.bisectors()[p]
        return MyLineSegment(bs.p1, MyPoint(bs.p2.x, bs.p2.y))

    def add_altitude(self, p):
        hs = self.altitudes[p]
        return MyLineSegment(hs.p1, MyPoint(hs.p2.x, hs.p2.y))

    def add_circumcircle(self):
        circumcenter = MyPoint(self.circumcenter.x, self.circumcenter.y)
        circumradius = self.circumradius.evalf()
        return MyCircle(circumcenter, circumradius)

    def add_incircle(self):
        incenter = MyPoint(self.incenter.x, self.incenter.y)
        inradius = self.inradius.evalf()
        return MyCircle(incenter, inradius)

    def add_medial(self):
        t = Triangle(*self.vertices).medial.vertices
        return MyTriangle(MyPoint(t[0].x, t[0].y), MyPoint(t[1].x, t[1].y), MyPoint(t[2].x, t[2].y))

    def add_eulerline(self):
        t = Triangle(*self.vertices).eulerline
        if (type(t) == type(Line((1, 2), (2, 3)))):
            return MyStraight(MyPoint(t.p1.x, t.p1.y), MyPoint(t.p2.x, t.p2.y))
        elif (type(t)== type(Point(1, 2))):
            return MyPoint(t.x, t.y)

    def add_ninepointcircle(self):
        c = self.nine_point_circle
        return MyCircle(MyPoint(c.center.coordinates), c.radius)


# для того, чтобы транслировать гиф картинку
class QMovieLabel(QLabel):
    def __init__(self, fileName, parent=None):
        super(QMovieLabel, self).__init__(parent)
        m = QtGui.QMovie(fileName)
        self.setMovie(m)
        m.start()

    def setMovie(self, movie):
        super(QMovieLabel, self).setMovie(movie)
        s = movie.currentImage().size()
        self._movieWidth = s.width()
        self._movieHeight = s.height()


class Library:
    pass


# метод получения треугольника
# x1, y1, x2, y2- координаты начала и конца области, в которой нужно построить треугольник
# k1-критерий соотношения сторон 0-разносторонний, 3-равносторонний, 4-равнобедренный
# k2-критерий определяющий тип треугольника по углам, 0-остроугольный,1-тупоугольный, 2-прямоугольный
def get_triangle(k1=0, k2=0, x1=100, y1=100, x2=300, y2=300):
    '''if names == None:
        names = sample(ALPHABET, 3)
    else:
        names = names.copy()'''
    corners, sides = get_corners_and_sides(k1, k2)
    p1 = MyPoint(x1, y2)
    p3 = MyPoint(x1 + sides[1], y2)
    c1 = MyCorner(corners[0], p1, p3, line=sides[2])
    p2 = c1.p3
    c2 = MyCorner(corners[1], p2, p1, line=sides[0])
    c3 = MyCorner(corners[2], p3, p2, line=sides[1])
    s1, s2, s3 = MyLineSegment(p2, p3), MyLineSegment(p3, p1),\
                 MyLineSegment(p1, p2)
    return MyTriangle(p1, p2, p3)


def get_corners_and_sides(k1, k2):
    with open("corners.txt", mode='r', encoding="utf8") as t:
        corners = list(map(lambda x: int(x), t.readlines()[k1 + k2].split()))
    s2 = 200
    s1 = 200 * sin(corners[0] * pi / 180) / sin(corners[1] * pi / 180)
    s3 = 200 * sin(corners[2] * pi / 180) / sin(corners[1] * pi / 180)
    return corners, [s1, s2, s3]


TRIANGLES = list(map(lambda x: get_triangle(k1=x[0], k2=x[1], x1=x[2], y1=x[3], x2=x[4], y2=x[5]),
                     [(0, 0, 50, 50, 250, 250), (0, 1, 350, 50, 550, 250),
                      (0, 2, 650, 50, 850, 250), (3, 0, 50, 350, 250, 550),
                      (4, 0, 350, 350, 550, 550), (4, 1, 650, 350, 850, 550),
                      (4, 2, 350, 650, 550, 850)]))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Work()
    ex.show()
    sys.exit(app.exec())

