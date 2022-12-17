from car import car
from constansts import acceleration_player_max, acceleration_player_min, player_rotation_rate
import pygame
from math import pi

class Player(car):
    '''
    Класс отвечающий за игрока.
    '''
    def __init__(self)->None:
        super().__init__(1000, 75, angle = pi, max_acceleration = acceleration_player_max, min_acceleration = acceleration_player_min)
        self.is_forward = False
        self.is_backward = False
        self.is_left = False
        self.is_right = False
        self.is_break = False

    def draw(self, surface)->None:
        '''
        Отрисовывает машину на pygame.surface
        '''
        pygame.draw.polygon(surface, (0, 255, 0), self.car_rect.get_points())

    def next_frame(self)->bool:
        '''
        Возвращает False, если машина разбилась
        иначе True
        '''
        if self.check_crash():
            return False

        if self.is_left:
            self.turn(player_rotation_rate * self.get_speed() / 5000)
        if self.is_right:
            self.turn(-player_rotation_rate * self.get_speed() / 5000)
        if self.is_forward:
            self.accelerate()
        if self.is_backward:
            self.slow_down()
        if self.is_break:
            self.break_()

        self.slow_down_by_drift()
        self.go()
        return True

    def update_event(self, event)->None:
        '''
        Обработка нажатий на клавиатуру
        '''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.is_forward = True
            if event.key == pygame.K_s:
                self.is_backward = True
            if event.key == pygame.K_a:
                self.is_left = True
            if event.key == pygame.K_d:
                self.is_right = True
            if event.key == pygame.K_SPACE:
                self.is_break = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.is_forward = False
            if event.key == pygame.K_s:
                self.is_backward = False
            if event.key == pygame.K_a:
                self.is_left = False
            if event.key == pygame.K_d:
                self.is_right = False
            if event.key == pygame.K_SPACE:
                self.is_break = False