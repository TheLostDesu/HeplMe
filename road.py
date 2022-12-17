from geometry import Polyline, Point
from constansts import road_inner_points, road_outer_points
import pygame

class Road():
    '''
    Класс отвечающий за дорогу.
    '''
    def __init__(self)->None:
        self.inner_poly = Polyline([Point(pnt[0], pnt[1]) for pnt in road_inner_points])
        self.outer_poly = Polyline([Point(pnt[0], pnt[1]) for pnt in road_outer_points])
    
    def draw(self, surface)->None:
        '''
        Отрисовка дороги на pygame surface
        '''
        for segment in self.inner_poly.get_segments():
            pygame.draw.aaline(surface, (0, 0, 0), segment.point1.get_coords(), segment.point2.get_coords())
        for segment in self.outer_poly.get_segments():
            pygame.draw.aaline(surface, (0, 0, 0), segment.point1.get_coords(), segment.point2.get_coords())
