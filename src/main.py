import os

import pygame
import neat

from neat_algo import FlappyNeat

from game.controllers import EnvController, ScoreController
from game.game_objects import Bird
from game.globals.constants import (
    GAME_FIELD_HEIGHT, GAME_FIELD_WIDTH
)

BG_IMAGE_PATH = os.path.join('..', 'data', 'sprites', 'background.png')
BACKGROUND_IMAGE = pygame.image.load(BG_IMAGE_PATH)

window = pygame.display.set_mode(
    (GAME_FIELD_WIDTH, GAME_FIELD_HEIGHT)
)


def draw_window(
        window: pygame.Surface,
        bird: Bird,
        env_controller: EnvController
    ) -> None:
    
    window.blit(BACKGROUND_IMAGE, (0, 0))
    bird.draw(window)
    env_controller.draw(window)


def main(agent):

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

        output = agent.activate((
                bird.position.y_top_pos,
                env_controller.neares_pipe_position.x_left_pos - bird.position.x_left_pos,
                env_controller.neares_pipe_position.y_top_pos - bird.position.y_top_pos,
                env_controller.neares_pipe_position.y_bottom_pos - bird.position.y_top_pos
            ))[0]

        if output > 0.5:
            bird.flap()

        env_controller.move()
        bird.move()

        score = env_controller.get_score(bird)

        if score == -1:
            bird = Bird()
            env_controller = EnvController()
            score_controller = ScoreController()
            score_global = 0

            continue

        if score == 1:
            score_global += 1

        draw_window(window, bird, env_controller)
        score_controller.draw(window, score_global)
        pygame.display.update()

if __name__ == '__main__':
    config_path = '../data/neat_config_files/config_feedforward.txt'

    flappy_neat = FlappyNeat(config_path, score_threshold=150)
    winner = flappy_neat.get_winner()

    main(winner)
