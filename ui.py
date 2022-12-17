import pygame
import pygame.locals
import variables
from logic import create_objects, next_frame, update_event
from constansts import FPS
from AI import agent_define

if __name__ == "__main__":
    pygame.init()
    agent_define()
    create_objects()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    variables.field_size_x, variables.field_size_y = screen.get_size()
    screen.fill((242,242,247))

    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill((242,242,247))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.locals.QUIT:
                running = False
            update_event(event)

        next_frame()

        for i in variables.objects:
            i.draw(screen)
        if variables.road is not None:
            variables.road.draw(screen)
        pygame.display.update()
        clock.tick(FPS)
    
    pygame.quit()
