# структура проекта
import sys
# import numpy as np
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt
from math import sin, cos, asin, pi, sqrt
from random import choice, sample


SCREEN_SIZE = [500, 500]
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
FIGURES = list()
RELATIONS = [[], []]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Рисование')
        self.po1 = Point('A', 100, 150)
        self.po2 = Point('B', 40, 190)
        self.t1 = get_triangle()
        self.b1 = self.t1.add_median(self.t1.p2, self.t1.s2, 'AC')

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
        self.t1.draw(qp)
        self.b1.draw(qp)

# класс точки на плоскости
class Point:
    def __init__(self, name, x, y):
        self.name = name
        self.x, self.y = x, y

    def draw(self, qp):
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        qp.setPen(pen)
        color = QColor(255, 255, 255)
        qp.setBrush(color)
        qp.drawEllipse(int(self.x - 2), int(self.y - 2), 4, 4)
        l = Letter(Point(self.name, self.x, self.y))
        l.draw(qp)

    def __lt__(self, other):
        if self.x < other.x and self.y < other.y:
            return True
        return False

    def __le__(self, other):
        if self.x <= other.x and self.y <= other.y:
            return True
        return False

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def __ne__(self, other):
        if self.x != other.x and self.y != other.y:
            return True
        return False

    def __gt__(self, other):
        if self.x > other.x and self.y > other.y:
            return True
        return False

    def __ge__(self, other):
        if self.x >= other.x and self.y >= other.y:
            return True
        return False

    def __str__(self):
        return self.name


# класс прямой на плоскости
class Straight:
    def __init__(self, name, p1, p2):
        self.name = name
        self.p1 = p1
        self.p2 = p2

    def draw(self, qp):
        pen = QPen(Qt.black, 2, Qt.DotLine)
        qp.setPen(pen)
        dx, dy = abs(self.p1.x - self.p2.x) // 2, abs(self.p1.y - self.p2.y) // 2
        x1, y1, x2, y2 = self.p1.x, self.p1.y, self.p2.x, self.p2.y
        if self.p1 >= self.p2:
            qp.drawLine(x1 + dx, y1 + dy, x2 - dx, y2 - dy)
        elif self.p1 <= self.p2:
            qp.drawLine(x1 - dx, y1 - dy, x2 + dx, y2 + dy)
        elif x1 <= x2 and y1 >= y2:
            qp.drawLine(x1 - dx, y1 + dy, x2 + dx, y2 - dy)
        elif x1 >= x2 and y1 <= y2:
            qp.drawLine(x1 + dx, y1 - dy, x2 - dx, y2 + dy)
        LineSegment(self.name, self.p1, self.p2).draw(qp)


# класс отрезка на плоскости
class LineSegment:
    def __init__(self, name, p1, p2):
        self.name = name
        self.p1 = p1
        self.p2 = p2
        self.s = self.get_lenght()

    def draw(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(int(self.p1.x), int(self.p1.y), int(self.p2.x), int(self.p2.y))
        pen.setStyle(Qt.DotLine)
        qp.setPen(pen)
        self.p1.draw(qp)
        self.p2.draw(qp)

    # функция, возвращающая длину отрезка
    def get_lenght(self):
        return sqrt((self.p1.x - self.p2.x) ** 2 + (self.p1.y - self.p2.y) ** 2)

    def __lt__(self, other):
        if self.s < other.s:
            return True
        return False

    def __le__(self, other):
        if self.s <= other.s:
            return True
        return False

    def __eq__(self, other):
        if self.s == other.s:
            return True
        return False

    def __ne__(self, other):
        if self.s != other.s:
            return True
        return False

    def __gt__(self, other):
        if self.s > other.s:
            return True
        return False

    def __ge__(self, other):
        if self.s >= other.s:
            return True
        return False


# класс луча на плоскости
class Ray:
    def __init__(self, name, p1, p2):
        self.name = name
        self.p1, self.p2 = p1, p2

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
        LineSegment(self.name, self.p1, self.p2).draw(qp)


# класс угла, который является частью замкнутой фигуры на плоскости
class Corner:
    def __init__(self, name, size, p1, p2, p3=None, line=None):
        self.name = name
        self.p1 = p1
        self.p2 = p2
        self.s = size
        if p3 == None:
            self.get_p3(line)

    def get_p3(self, line=None):
        # plotting self.p3 of a given value using the math library
        if line == None:
            line = LineSegment(str(self.p1) + str(self.p2), self.p1, self.p2).get_lenght()
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
        self.p3 = Point(self.name[2], m[0], m[1])

    def draw(self, qp):
        LineSegment(self.name[1::-1], self.p1, self.p2).draw(qp)
        LineSegment(self.name[1:], self.p1, self.p3).draw(qp)


# класс угла как геометрической фигуры на плоскости
class Geometric_Corner(Corner):
    def __init__(self, name, p1, p2, size):
        super().__init__(name, p1, p2, size)

    def draw(self, qp):
        Ray(self.name[1::-1], self.p1, self.p2).draw(qp)
        Ray(self.name[1:], self.p1, self.p3).draw(qp)


class Сircle:
    def __init__(self, p, r):
        self.p = p
        self.r = r

    def draw(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawEllipse(QRect(self.p.x - self.r, self.p.y - self.r, self.p.x + self.r, self.p.y + self.r))


# класс треугольника как геометрической фигуры на плоскости
class Triangle:
    def __init__(self, p1=None, p2=None, p3=None,
                 s1=None, s2=None, s3=None, c1=None, c2=None, c3=None):
        self.p1, self.p2, self.p3 = p1, p2, p3
        self.s1, self.s2, self.s3 = s1, s2, s3
        self.c1, self.c2, self.c3 = c1, c2, c3

    def draw(self, qp):
        self.s1.draw(qp)
        self.s2.draw(qp)
        self.s3.draw(qp)

    def continue_side(self, s, p):
        pass

    def get_corners(self):
        pass

    def add_bisector(self, p, s, c, name):
        pass

    def add_height(self, p, s, c, c1, name):
        pass

    def add_median(self, p, s, name):
        return Median(name, p, Point(name[1], min(s.p1.x, s.p2.x) + abs(s.p1.x - s.p2.x) / 2,
                                     min(s.p1.y, s.p2.y) + abs(s.p1.y - s.p2.y) / 2))

    # добавить вписанную окружность
    def add_inscribed_circle(self):
        pass

    # добавить описанную окружность
    def add_circumscribed_circle(self):
        pass



# класс биссектрисы как отрезка в треугольнике, __init__ и draw() наследуются от класса-родителя LineSegment
class Bisector(LineSegment):
    def __init__(self, name, p1, p2):
        super().__init__(name, p1, p2)



# класс высоты в треугольнике, __init__ и draw() наследуются от класса-родителя LineSegment
class Height(LineSegment):
    def __init__(self, name, p1, p2):
        super().__init__(name, p1, p2)


# класс медианы в треугольнике, __init__ и draw() наследуются от класса-родителя LineSegment
class Median(LineSegment):
    def __init__(self, name, p1, p2):
        super().__init__(name, p1, p2)


# класс буквы создан для того, чтобы обозначать именами точки на рисунке
class Letter:
    def __init__(self, point):
        self.point = point

    def draw(self, qp):
        pen = QPen(Qt.black, 2, Qt.DotLine)
        qp.setPen(pen)
        qp.drawText(self.point.x - 10, self.point.y - 10, str(self.point))


# проверка неравенства треугольника
def get_triangle_inequality(a, b, c):
    return all((self.a.s + self.b.s > self.c.s), (self.b.s + self.c.s > self.a.s), (self.a.s + self.c.s > self.b.s))


# метод получения треугольника
# x1, y1, x2, y2- координаты начала и конца области, в которой нужно построить треугольник
# k1-критерий соотношения сторон 0-разносторонний, 3-равносторонний, 4-равнобедренный
# k2-критерий определяющий тип треугольника по углам, 0-остроугольный,1-тупоугольный, 2-прямоугольный
def get_triangle(names=None, k1=1, k2=0, x1=100, y1=100, x2=300, y2=300):
    if names == None:
        names = sample(ALPHABET, 3)
    corners, sides = get_corners_and_sides(k1, k2)
    p1 = Point(names[0], x1, y2)
    p3 = Point(names[2], x1 + sides[1], y2)
    c1 = Corner(names[2] + names[0] + names[1], corners[0], p1, p3, line=sides[2])
    p2 = c1.p3
    c2 = Corner(names[0] + names[1] + names[2], corners[1], p2, p1, line=sides[0])
    c3 = Corner(names[1] + names[2] + names[0], corners[2], p3, p2, line=sides[1])
    s1, s2, s3 = LineSegment(names[1] + names[2], p2, p3), LineSegment(names[2] + names[0], p3, p1),\
                 LineSegment(names[0] + names[1], p1, p2)
    return Triangle(p1, p2, p3, s1, s2, s3, c1, c2, c3)


def get_corners_and_sides(k1, k2):
    with open("corners.txt", mode='r', encoding="utf8") as t:
        corners = list(map(lambda x: int(x), t.readlines()[k1 + k2].split()))
    s2 = 200
    s1 = 200 * sin(corners[0] * pi / 180) / sin(corners[1] * pi / 180)
    s3 = 200 * sin(corners[2] * pi / 180) / sin(corners[1] * pi / 180)
    return corners, [s1, s2, s3]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
