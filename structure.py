# структура проекта
import sys
# import numpy as np
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt
import math

SCREEN_SIZE = [500, 500]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Рисование')
        self.po1 = Point('A', 10, 10)
        self.po2 = Point('B', 10, 300)
        self.r = Corner('ABC', self.po1, self.po2, 30)

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
        self.r.draw(qp)


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


class LineSegment:
    def __init__(self, name, p1, p2):
        self.name = name
        self.p1 = p1
        self.p2 = p2

    def draw(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(int(self.p1.x), int(self.p1.y), int(self.p2.x), int(self.p2.y))
        pen.setStyle(Qt.DotLine)
        qp.setPen(pen)
        self.p1.draw(qp)
        self.p2.draw(qp)


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


class Corner:
    def __init__(self, name, p1, p2, size):
        self.name = name
        self.p1 = p1
        self.p2 = p2
        self.s = size

    def draw(self, qp):
        # plotting the angle of a given value using the math library
        line = math.sqrt((self.p2.x - self.p1.x) ** 2 + (self.p2.y - self.p1.y) ** 2)
        m = [self.p2.x + line * math.cos(self.s * math.pi / 180),
             line * math.sin(self.s * math.pi / 180) + self.p2.y]
        p3 = Point(self.name[2], m[0], m[1])
        Ray(self.name[1::-1], self.p1, self.p2).draw(qp)
        Ray(self.name[1:], self.p1, p3).draw(qp)


class Triangle:
    def __init__(self, p1=Point('A', 50, 50), p2=Point('B', 100, 100), p3=Point('C', 50, 150),
                 s1=1, s2=1, s3=1, c1=45, c2=90, c3=45):
        self.p1, self.p2, self.p3 = p1, p2, p3
        self.s1, self.s2, self.s3 = s1, s2, s3
        self.c1, self.c2, self.c3 = c1, c2, c3

    def draw(self, qp):
        LineSegment(str(self.p1) + str(self.p2), self.p1, self.p2).draw(qp)
        LineSegment(str(self.p2) + str(self.p3), self.p2, self.p3).draw(qp)
        LineSegment(str(self.p3) + str(self.p1), self.p3, self.p1).draw(qp)


class Bisector:
    def __init__(self, name, tr):
        self.name, self.tr = name, tr

    def get_lenght(self):
        pass

    def draw(self):
        pass


class Height:
    def __init__(self, name, tr):
        self.name, self.tr = name, tr

    def get_lenght(self):
        pass

    def draw(self):
        pass


class Median:
    def __init__(self, name, tr):
        self.name, self.tr = name, tr

    def get_lenght(self):
        pass

    def draw(self):
        pass



class Letter:
    def __init__(self, name, x, y):
        self.name = name
        self.x, self.y = x, y

    def draw(self, qp):
        pen = QPen(Qt.black, 2, Qt.DotLine)
        qp.setPen(pen)
        qp.drawText(self.x, self.y, self.name)


# function for getting the x coordinate on the screen
def xs(x):
    return x + SCREEN_SIZE[0] // 2


# function for getting the y coordinate on the screen
def ys(y):
    return SCREEN_SIZE[1] // 2 - y


# matrix and vector multiplication function
def product_of_matrix_by_vector(a, b):
    total = a.dot(b)
    return total


# the generating function of the vector
def creating_vector(x, y):
    return np.array([[x], [y]])


# function for creating a rotation matrix
def rotation_matrix(alpha):
    a = math.radians(alpha)
    matrix = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
    return matrix


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
