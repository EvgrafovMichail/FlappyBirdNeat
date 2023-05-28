import os

import pygame

from game.controllers import EnvController, ScoreController
from game.game_objects import Bird
from game.globals.constants import (
    GAME_FIELD_HEIGHT, GAME_FIELD_WIDTH
)

BG_IMAGE_PATH = os.path.join('..', 'data', 'sprites', 'background.png')
BACKGROUND_IMAGE = pygame.image.load(BG_IMAGE_PATH)


def draw_window(
        window: pygame.Surface,
        bird: Bird,
        env_controller: EnvController
    ) -> None:
    
    window.blit(BACKGROUND_IMAGE, (0, 0))
    bird.draw(window)
    env_controller.draw(window)


def main():

    window = pygame.display.set_mode(
        (GAME_FIELD_WIDTH, GAME_FIELD_HEIGHT)
    )
    clock = pygame.time.Clock()
    
    bird = Bird()
    env_controller = EnvController()
    score_controller = ScoreController()
    score_global = 0

    while True:

        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                bird.flap()

        env_controller.move()
        bird.move()

        score = env_controller.get_score(bird)

        if score == -1000:
            bird = Bird()
            env_controller = EnvController()
            score_controller = ScoreController()
            score_global = 0

            continue
        
        elif score == 1:
            score_global += 1

        draw_window(window, bird, env_controller)
        score_controller.draw(window, score)
        pygame.display.update()

if __name__ == '__main__':
    main()
