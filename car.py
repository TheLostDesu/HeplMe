from constansts import car_size_x, car_size_y, FPS
from math import sin, cos
from geometry import Rectangle, Point, Segment
import variables


class car():
    '''
    Базовый класс машины.
    '''
    def __init__(self, x, y, angle = 0, speed_x = 0, speed_y = 0, max_acceleration = 0, min_acceleration = 0,
                 maximal_speed = 1000, grip = 3):
        self.car_rect = Rectangle(point1 = Point(x, y), lenx = car_size_x, leny = car_size_y)
        self.car_rect.rotate(angle)
        self.angle = angle
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.max_acceleration = max_acceleration
        self.min_acceleration = min_acceleration
        self.maximal_speed = maximal_speed
        self.grip = grip

    def go(self):
        '''
        Функция, перемещающая машину на нужное расстояние
        '''
        if abs(self.speed_x) > 1:
            self.car_rect.move(self.speed_x // FPS, 0)
        if abs(self.speed_y) > 1:
            self.car_rect.move(0, self.speed_y // FPS)
    
    def turn(self, angle):
        '''
        Функция поворота машины
        '''
        self.angle += angle
        self.car_rect.rotate(angle)
    
    def check_crash(self):
        '''
        Проверка машины на столкновение
        '''
        if variables.road is not None:
            return (len(self.car_rect.intersect_poly(variables.road.outer_poly)) != 0 
                or len(self.car_rect.intersect_poly(variables.road.inner_poly)) != 0)
    
    def get_speed2(self):
        '''
        Возвращает скорость в квадрате
        '''
        return self.speed_x ** 2 + self.speed_y**2
    
    def get_speed(self):
        '''
        Возвращает скорость
        '''
        return self.get_speed2() ** 0.5

    def speed_max_check(self):
        '''
        Проверяет, превышена ли максимальная скорость машины.
        '''
        return self.get_speed2() <= self.maximal_speed ** 2 

    def accelerate(self):
        '''
        Ускоряет машину (как при нажатии на кнопку w)
        '''
        self.speed_y -= self.max_acceleration * sin(self.angle)
        self.speed_x += self.max_acceleration * cos(self.angle)
        if not self.speed_max_check():
            k = self.get_speed2() / self.maximal_speed**2
            self.speed_x /= k
            self.speed_y /= k

    def slow_down(self):
        '''
        Замедляет машину (Как при нажатии на кнопку s)
        '''
        self.speed_y -= self.min_acceleration * sin(self.angle)
        self.speed_x += self.min_acceleration * cos(self.angle)
        if not self.speed_max_check():
            k = self.get_speed() / self.maximal_speed 
            self.speed_x /= k
            self.speed_y /= k
    
    def break_(self):
        '''
        Очень быстро замедляет машину (Как при нажатии на кнопку пробела)
        '''
        self.speed_y /= 1.5
        self.speed_x /= 1.5

    def slow_down_by_drift(self):
        '''
        Меняет вектор машины, если она повернула. Нужен чтобы поворот не осуществлялся мнгновенно,
        а происходило скольжение.
        '''
        if self.get_speed2() > 10:
            spd = self.get_speed()

            for _ in range(self.grip):
                self.speed_y -= self.max_acceleration * sin(self.angle)
                self.speed_x += self.max_acceleration * cos(self.angle)
            
            dspeed_x = self.get_speed() / spd
            self.speed_y /= self.get_speed() / spd
            self.speed_x /= dspeed_x
            