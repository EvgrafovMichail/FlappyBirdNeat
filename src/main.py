import os

import pygame

from game.game_objects import Bird, PipesPair, Floor
from game.globals.constants import (
    GAME_FIELD_HEIGHT, GAME_FIELD_WIDTH
)

os.listdir('../data/sprites')

BG_IMAGE_PATH = os.path.join('..', 'data', 'sprites', 'background.png')
BACKGROUND_IMAGE = pygame.image.load(BG_IMAGE_PATH)


def draw_window(window: pygame.Surface, bird: Bird, pipes, floor):
    
    window.blit(BACKGROUND_IMAGE, (0, 0))
    bird.draw(window)

    for pipe in pipes:
        pipe.draw(window)

    floor.draw(window)
    pygame.display.update()


def main():

    window = pygame.display.set_mode(
        (GAME_FIELD_WIDTH, GAME_FIELD_HEIGHT)
    )
    clock = pygame.time.Clock()
    bird = Bird()
    floor = Floor()
    pipes = [PipesPair()]

    while True:

        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                bird.flap()

        pipe_to_delete = None
        for pipe in pipes:
            pipe.move()

            if pipe.x + 52 < 0:
                pipe_to_delete = pipe

        if pipe_to_delete:
            pipes.remove(pipe_to_delete)
            pipes.append(PipesPair())

        floor.move()
        bird.move()

        draw_window(window, bird, pipes, floor)

if __name__ == '__main__':
    main()
