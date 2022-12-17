from geometry import Rectangle, Point

class checkpoint():
    '''
    Чекпоинт который говорит, что ИИ все делает ок
    '''
    def __init__(self, x:int, y:int)->None:
        self.is_used = False
        self.checkpnt_rect = Rectangle(point1=Point(x, y), lenx = 100, leny = 100)
    
    def use(self) -> None:
        '''
        Переключает состояние used
        '''
        self.is_used = True
    
    def unuse(self)->None:
        '''
        Переключает состояние used
        '''
        self.is_used = False