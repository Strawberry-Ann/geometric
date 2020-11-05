class Point:
    def __init__(self, name, x, y):
        self.name = name
        self.x, self.y = x, y

    def draw(self):
        pass


class Straight:
    def __init__(self, name, p1, p2):
        self.name = name
        self.p1 = p1
        self.p2 = p2


class LineSegment:
    def __init__(self, name, p1, p2):
        self.name = name
        self.p1 = p1
        self.p2 = p2


class Ray:
    def __init__(self, name, p1):
        self.name = name
        self.p1 = p1


class Corner:
    def __init__(self, p1, p2, p3, size):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.size = size


class Triangle:
    def __init__(self, p1='A', p2='B', p3='C',
                 s1='1', s2=1, s3=1, c1=60, c2=60, c3=60):
        self.p1, self.p2, self.p3 = p1, p2, p3
        self.s1, self.s2, self.s3 = s1, s2, s3
        self.c1, self.c2, self.c3 = c1, c2, c3

