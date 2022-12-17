from math import sin, cos
from constansts import epsilon

def is_equal(a:float, b:float)->bool:
    '''
    Проверка на примерное равенство двух значений типа float
    '''
    return abs(a - b) < epsilon

class Point():
    '''
    Базовый клас задающий точку.
    '''
    def __init__(self, x:float, y:float)->None:
        self.x, self.y = x, y
    
    def get_x(self)->float:
        '''
        Возвращает координату x
        '''
        if self.x is None:
            return 0
        else:
            return self.x
    
    def get_y(self)->float:
        '''
        Возвращает координату y точки
        '''
        if self.y is None:
            return 0
        else:
            return self.y
    
        
    def get_coords(self):
        '''
        Возвращает координаты точки
        '''
        return (self.x, self.y)

    def set_x(self, x:float)->None:
        '''
        Задает координату x
        '''
        assert type(x) == float or type(x) == int
        set.x = x

    def set_y(self, y:float)->None:
        '''
        Задает координату y
        '''
        assert type(y) == float or type(y) == int
        self.y = y
    
    def __eq__(self, other) -> bool:
        assert type(self) == type(other)
        return is_equal(self.x, other.x) and is_equal(self.y, other.y)
    
    def __ne__(self, other) -> bool:
        assert type(self) == type(other)
        return not self.__eq__(other)

    def __str__(self) -> str:
        return "point (" + str(self.x) + ", " + str(self.y) + ")"
    
    def __add__(self, other):
        assert type(self) == type(other)
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        assert type(self) == type(other)
        return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        assert type(self) == type(other)
        return self.x * other.x + self.y * other.y
    
    def __xor__(self, other):
        assert type(self) == type(other)
        return self.x * other.y - self.y * other.x
    
    def __mod__(self, other):
        assert type(self) == type(other)
        return Point((self.x + other.get_x()) / 2, (self.y + other.get_y()) / 2)

    def dist2(self, other) -> float:
        assert type(self) == type(other)
        '''
        Возвращает расстояние до точки в квадрате.
        '''
        return (self.x - other.x)**2 + (self.y - other.y)**2
    
    def is_parallel(self, other)->bool:
        assert type(self) == type(other)
        '''
        Проверяет, параллельны ли два вектора с концами в этих двух точках
        '''
        return is_equal(self ^ other, 0)
    
    def rotate(self, center, angle:float):
        assert type(self) == type(center)
        assert type(angle) == int or type(angle) == float
        '''
        Поворачивает точку относительно точки center на угол angle
        '''
        centered_p = self - center
        self.x = center.get_x() + centered_p.get_x() * cos(angle) + centered_p.get_y() * sin(angle)
        self.y = center.get_y() + centered_p.get_y() * cos(angle) - centered_p.get_x() * sin(angle)


class Line():
    '''
    Базовый класс задающий прямую вида ax + by + c = 0
    '''
    def __init__(self, point1:Point = None, point2:Point = None, a:float = None, b:float = None, c:float = None)->None:
        if a is not None and b is not None and c is not None:
            assert type(a) == float or type(a) == int
            assert type(b) == float or type(b) == int
            assert type(c) == float or type(c) == int
            self.a = a
            self.b = b
            self.c = c
        elif point1 is not None and point2 is not None:
            self.a = point1.get_y() - point2.get_y()
            self.b = point2.get_x() - point1.get_x()
            self.c = -(self.a * point1.get_x() + self.b * point1.get_y())
        
        assert(False, 'Line is not defined')
    
    def get_parallel_vector(self) -> Point:
        '''
        Возвращает координаты вектора параллельного этой прямой.
        '''
        return Point(-self.b, self.a)

    def is_parallel(self, other) -> bool:
        '''
        Проверяет, паралелльны ли две прямые.
        '''
        assert type(self) == type(other)
        return self.get_parallel_vector().is_parallel(other.get_parallel_vector())

    def __xor__(self, other)->Point:
        '''
        Возвращает None если две прямые параллельны
        Иначе возвращает точку в которой они пересекаются
        '''
        assert type(self) == type(other)

        if self.is_parallel(other):
            return None
        
        if self.a != 0:
            y_int = (self.c * other.a / self.a - other.c) / (other.b - other.a * self.b / self.a)
            x_int = -(self.b * y_int + self.c) / self.a
        else:
            y_int = -self.c / self.b
            x_int = -(other.b * y_int + other.c) / other.a
        
        return Point(x_int, y_int)


class Segment():
    '''
    Базовый класс отрезка, заданный двумя точками.
    '''
    def __init__(self, point1:Point, point2:Point):
        self.point1 = point1
        self.point2 = point2

    def get_up(self)->float:
        '''
        возвращает верхнюю границу отрезка
        '''
        return max(self.point1.get_y(), self.point2.get_y())
    
    def get_down(self)->float:
        '''
        возвращает нижнюю границу отрезка(В координатах реального мира, а не pygame)
        '''
        return min(self.point1.get_y(), self.point2.get_y())
    
    def get_right(self)->float:
        '''
        возвращает правую границу отрезка
        '''
        return max(self.point1.get_x(), self.point2.get_x())
    
    def get_left(self)->float:
        '''
        возвращает левую границу отрезка
        '''
        return min(self.point1.get_x(), self.point2.get_x())

    def is_in(self, point:Point)->bool:
        '''
        Проверяет, лежит ли точка на отрезке, если она лежит на прямой этого
        '''
        if point == self.point1 or point == self.point2:
            return True

        return (point.get_x() >= self.get_left() and point.get_x() <= self.get_right() and
                point.get_y() >= self.get_down() and point.get_y() <= self.get_up())


    def __eq__(self, other)->bool:
        assert type(self) == type(other)
        return self.point1 == other.point1 and self.point2 == other.point2

    def __str__(self)->str:
        return 'Segment('+str(self.point1) + ', '+ str(self.point2) + ')'

    def __xor__(self, other)->Point:
        '''
        Если два отрезка не пересекаются возвращает None
        Иначе возвращает Point их пересечения.
        '''
        assert type(self) == type(other)
        line1 = Line(point1=self.point1, point2=self.point2)
        line2 = Line(point1=other.point1, point2=other.point2)
        pnt = line1 ^ line2
        if pnt is None:
            return None
        if self.is_in(pnt) and other.is_in(pnt):
            return pnt
        return None
    
    def rotate(self, center:Point, angle:float) -> None:
        '''
        Поворачивает отрезок относительно точки center
        На угол angle
        '''
        assert type(angle) == float or type(angle) == int
        self.point1.rotate(center, angle)
        self.point2.rotate(center, angle)




class Rectangle():
    '''
    Базовый класс прямоугольника, заданный двумя точками, либо точкой и длинной, и углом поворота.
    '''
    def __init__(self, point1:Point = None, point2:Point = None, lenx:float = None, leny:float = None)->None:
        assert point1 is not None
        assert point2 is not None or (lenx is not None and leny is not None)
        self.point1 = point1
        
        if point2 is None:
            self.point3 = Point(self.point1.get_x() + lenx, self.point1.get_y() + leny)
        else:
            self.point3 = point2
        
        self.point2 = Point(self.point1.get_x(), self.point3.get_y())
        self.point4 = Point(self.point3.get_x(), self.point1.get_y())

    def rotate(self, angle:float, center:Point = None)->None:
        '''
        Поворачивает прямоугольник относительно центра. 
        Если центр не выбран - выбирает центр прямоугольника по умолчанию
        '''
        if center is None:
            center = self.point1 % self.point3
        self.point1.rotate(center, angle)
        self.point2.rotate(center, angle)
        self.point3.rotate(center, angle)
        self.point4.rotate(center, angle)

    def move(self, x:float, y:float)->None:
        '''
        Перемещает прямоугольник по x и y
        '''
        assert type(x) == float or type(x) == int
        assert type(y) == float or type(y) == int
        self.point1 += Point(x, y)
        self.point2 += Point(x, y)
        self.point3 += Point(x, y)
        self.point4 += Point(x, y)
    
    def __xor__(self, other)->list:
        '''
        Возвращает list из всех точек пересечения двух прямоугольников.
        '''
        assert type(self) == type(other)
        segments_self = [Segment(self.point1, self.point2), Segment(self.point2, self.point3), 
                         Segment(self.point3, self.point4), Segment(self.point4, self.point1)]
        segments_other = [Segment(other.point1, other.point2), Segment(other.point2, other.point3), 
                         Segment(other.point3, other.point4), Segment(other.point4, other.point1)]  
        intersections = []
        for i in segments_self:
            for j in segments_other:
                if i ^ j is not None:
                    intersections.append(i ^ j)
        return intersections
    
    def intersect_poly(self, polyline)->list:
        '''
        Пересекает прямоугольник с ломаной линией. Возвращает list всех пересечений.
        '''
        segments_self = [Segment(self.point1, self.point2), Segment(self.point2, self.point3), 
                         Segment(self.point3, self.point4), Segment(self.point4, self.point1)]  
        intersections = []
        for i in segments_self:
            for j in polyline.get_segments():
                if i ^ j is not None:
                    intersections.append(i ^ j)
        return intersections

    def get_points(self)->tuple:
        return (self.point1.get_coords(), self.point2.get_coords(),
                self.point3.get_coords(), self.point4.get_coords())

class Polyline():
    '''
    Базовый класс ломаной линии.
    '''
    def __init__(self, points:list)->None:
        assert len(points) > 1
        self.segments = []
        for i in range(1, len(points)):
            self.segments.append(Segment(points[i - 1], points[i]))
    
    def get_segments(self)->list:
        '''
        Возвращает список из отрезков входящих в ломаную
        '''
        return self.segments

class Ray():
    '''
    Базовый класс луча
    '''
    def  __init__(self, point_s:Point, point2:Point)->None:
        self.point_s = point_s
        self.point2 = point2
        self.line = Line(point1=self.point_s, point2=self.point2)
    
    def intersect_with_segment(self, segment:Segment)->Point:
        '''
        Пересечение луча и отрезка
        '''
        line = Line(point1=segment.point1, point2=segment.point2)
        pnt = self.line ^ line
        if pnt is None:
            return None
        if segment.is_in(pnt):
            if pnt.dist2(self.point2) < pnt.dist2(self.point_s):
                return pnt
        return None