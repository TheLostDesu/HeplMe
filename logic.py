from player import Player
from AI import AI_car, new_car
from road import Road
from variables import objects
import variables
import constansts
from checkpoint import checkpoint

def create_objects()->None:
    '''
    Создание всех объектов присутствующих в игре:
    Игрока
    Бота
    Дороги
    Чекпоинтов
    '''
    objects.append(Player())
    objects.append(AI_car())
    variables.road = Road()
    for i in constansts.checkpoints:
        variables.checkpoints.append(checkpoint(i[0], i[1]))



def update_event(event)->None:
    '''
    При поступлении какой-то информации с клавиатуры - передает ее в класс Player-а
    '''
    objects[0].update_event(event)

def next_frame()->None:
    '''
    Обрабатывает все, что случилось за этот фрейм с объектами. 
    Удаляет объекты, которые перестали быть нужными.
    '''
    to_delete = []
    for object_n in range(len(objects)):
        if not(objects[object_n].next_frame()):
            to_delete.append(object_n)
    for i in to_delete[::-1]:
        if i != 0:
            del(objects[i])
            
    if len(objects) == 1:
        objects.append(AI_car())
        new_car()
    
    if 0 in to_delete:
        del(objects[0])
        objects.insert(0, Player())
    
    k = 0
    for i in variables.checkpoints:
        if not i.is_used:
            k = 1
            break
    if k == 0: 
        for i in variables.checkpoints:
            i.unuse()
    

    
    return None