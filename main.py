# I am author!
import sys
import math
from PyQt5.QtGui import QPainter, QColor
from PyQt5 import uic
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QRect
from math import sin, cos, asin,  pi, sqrt
from random import sample
from sympy import *
from sympy.geometry import *


# a list of tuples, each representing the sequence of opening files
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
FIGURES = list()
TRIANGLES = list()


class FirstForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('test.ui', self)
        # Загружаем дизайн
        self.initUI()
        self.t = True

    def initUI(self):
        self.pb_OK.clicked.connect(self.f)

    def f(self):
        ex1 = SecondForm()
        ex.hide()
        ex1.show()


class SecondForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('1.ui', self)
        # Загружаем дизайн
        self.initUI()
        self.t = True

    def initUI(self):
        self.pb_OK.clicked.connect(self.get_information)

    def get_information(self):
        try:
            name = list(self.name.text())
            h = self.heights.text().strip().split()
            m = self.medians.text().strip().split()
            b = self.bisectors.text().strip().split()
            # s = self.simedians.text().strip().split()
            i_c = self.inscribed_circle.text().strip()
            c_c = self.circumscribed_circle.text().strip().split()
            if any([len(name) > 3, len(h) > 3, len(m) > 3, len(b) > 3, len(s) > 3, len(i_c) > 1, len(c_c) > 3]):
                raise FormatError('Введено неверное количество элементов')
            for k1, k2, x1, y2 in [(0, 0, 100, 300), (0, 1, 400, 300), (0, 2, 700, 300),
                                   (3, 0, 100, 600), (4, 0, 400, 600), (4, 1, 700, 600),
                                   (4, 2, 100, 900)]:
                TRIANGLES.append(get_triangle((name[0], name[1], name[2]), k1=k1, k2=k2, x1=x1, y2=y2))
            for t in TRIANGLES:
                for name_o in i_c:
                    FIGURES.append(t.add_inscribed_circle(name_o))
                for name_o in c_c:
                    FIGURES.append(t.add_circumscribed_circle(name_o))
                for name in h:
                    FIGURES.append(t.add_height(name))
                for name in m:
                    FIGURES.append(t.add_median(name))
                for name in b:
                    FIGURES.append(t.add_bisector(name))
        except FormatError as f:
            self.lb.setText(f'Ошибка! {f}')
        self.t = False
        ex.hide()
        ex2 = Example()
        ex2.show()


class FormatError(Exception):
    pass


class Drawing(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 1000, 1000)
        self.setWindowTitle('Рисование')

    # Метод срабатывает, когда виджету надо
    # перерисовать свое содержимое,
    # например, при создании формы
    def paintEvent(self, event):
        # Создаем объект QPainter для рисования
        qp = QPainter()
        # Начинаем процесс рисования
        qp.begin(self)
        self.draw_flag(qp)
        # Завершаем рисование
        qp.end()

    def draw_flag(self, qp):
        for figure in FIGURES:
            figure.draw(qp)


# класс точки на плоскости
class MyPoint(Point2D):
    def draw(self, qp):
        # нарисуем точку в виде пустого круга с толщиной линии 1
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        qp.setPen(pen)
        color = QColor(255, 255, 255)
        qp.setBrush(color)
        qp.drawEllipse(int(self.x - 2), int(self.y - 2), 4, 4)


# класс прямой на плоскости
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


# класс отрезка на плоскости
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


# класс луча на плоскости
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


# класс угла, который является частью замкнутой фигуры на плоскости
class MyCorner:
    def __init__(self, name, size, p1, p2, line=None):
        self.name = name
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
        self.p3 = MyPoint(self.name[2], m[0], m[1])

    def draw(self, qp):
        MyLineSegment(self.name[1::-1], self.p1, self.p2).draw(qp)
        MyLineSegment(self.name[1:], self.p1, self.p3).draw(qp)


# класс угла как геометрической фигуры на плоскости
class MyGeometricCorner(MyCorner):
    def __init__(self, name, p1, p2, size):
        super().__init__(name, p1, p2, size)

    def draw(self, qp):
        MyRay(self.name[1::-1], self.p1, self.p2).draw(qp)
        MyRay(self.name[1:], self.p1, self.p3).draw(qp)


# класс окружности
class MyCircle(Circle):
    def __init__(self, center, radius):
        Circle.__init__(center, radius, radius)

    def draw(self, qp):
        pen = QPen(Qt.black, 2, Qt.DotLine)
        qp.setPen(pen)
        r = self.hradius
        qp.drawEllipse(self.center.x - r, self.center.y - r, self.hradius * 2, self.vradius * 2)
        self.center.draw(qp)


# класс треугольника как геометрической фигуры на плоскости
class MyTriangle(Triangle):
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



# класс биссектрисы как отрезка в треугольнике, __init__ и draw() наследуются от класса-родителя LineSegment
class MyBisector(MyLineSegment):
    def __init__(self, name, p1, p2):
        super().__init__(name, p1, p2)


# класс высоты в треугольнике, __init__ и draw() наследуются от класса-родителя LineSegment
class MyHeight(MyLineSegment):
    def __init__(self, name, p1, p2):
        super().__init__(name, p1, p2)


# класс медианы в треугольнике, __init__ и draw() наследуются от класса-родителя LineSegment
class MyMedian(MyLineSegment):
    def __init__(self, name, p1, p2):
        super().__init__(name, p1, p2)


# класс буквы создан для того, чтобы обозначать именами точки на рисунке
class MyLetter:
    def __init__(self, name, x, y):
        self.name = name
        self.x, self.y = x, y

    def draw(self, qp):
        pen = QPen(Qt.black, 2, Qt.DotLine)
        qp.setPen(pen)
        qp.drawText(self.x, self.y, self.name)


# проверка неравенства треугольника
def get_triangle_inequality(a, b, c):
    return all((a.s + b.s > c.s), (b.s + c.s > a.s), (a.s + c.s > b.s))


# метод получения треугольника
# x1, y1, x2, y2- координаты начала и конца области, в которой нужно построить треугольник
# k1-критерий соотношения сторон 0-разносторонний, 3-равносторонний, 4-равнобедренный
# k2-критерий определяющий тип треугольника по углам, 0-остроугольный,1-тупоугольный, 2-прямоугольный
def get_triangle(names=('A', 'B', 'C'), k1=0, k2=0, x1=100, y1=100, x2=300, y2=300):
    if names == None:
        names = sample(ALPHABET, 3)
    else:
        names = names.copy()
    corners, sides = get_corners_and_sides(k1, k2)
    p1 = MyPoint(names[0], x1, y2)
    p3 = MyPoint(names[2], x1 + sides[1], y2)
    c1 = MyCorner(names[2] + names[0] + names[1], corners[0], p1, p3, line=sides[2])
    p2 = c1.p3
    c2 = MyCorner(names[0] + names[1] + names[2], corners[1], p2, p1, line=sides[0])
    c3 = MyCorner(names[1] + names[2] + names[0], corners[2], p3, p2, line=sides[1])
    s1, s2, s3 = MyLineSegment(names[1] + names[2], p2, p3), MyLineSegment(names[2] + names[0], p3, p1),\
                 MyLineSegment(names[0] + names[1], p1, p2)
    return MyTriangle(p1, p2, p3, s1, s2, s3, c1, c2, c3)


def get_corners_and_sides(k1, k2):
    with open("corners.txt", mode='r', encoding="utf8") as t:
        corners = list(map(lambda x: int(x), t.readlines()[k1 + k2].split()))
    s2 = 200
    s1 = 200 * sin(corners[0] * pi / 180) / sin(corners[1] * pi / 180)
    s3 = 200 * sin(corners[2] * pi / 180) / sin(corners[1] * pi / 180)
    return corners, [s1, s2, s3]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FirstForm()
    ex.show()
    sys.exit(app.exec())

