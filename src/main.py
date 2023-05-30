import sys
import os

import pygame
import neat

from neat_algo import FlappyNeat

from game.controllers import EnvController, ScoreController
from game.game_objects import Bird
from game.globals.constants import (
    GAME_FIELD_HEIGHT, GAME_FIELD_WIDTH, FPS
)


def main(agent: neat.nn.FeedForwardNetwork) -> None:

    bg_image_path = os.path.join('..', 'data', 'sprites', 'background.png')
    background_image = pygame.image.load(bg_image_path)

    window = pygame.display.set_mode(
        (GAME_FIELD_WIDTH, GAME_FIELD_HEIGHT)
    )

    clock = pygame.time.Clock()
    
    bird = Bird()
    env_controller = EnvController()
    score_controller = ScoreController()
    score_global = 0

    while True:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        output = agent.activate((
                bird.velocity,
                env_controller.nearest_pipe_position.x_left_pos - bird.position.x_left_pos,
                env_controller.nearest_pipe_position.y_top_pos - bird.position.y_top_pos,
                env_controller.nearest_pipe_position.y_bottom_pos - bird.position.y_top_pos
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

        window.blit(background_image, (0, 0))
        bird.draw(window)
        env_controller.draw(window)
        score_controller.draw(window, score_global)

        pygame.display.update()

if __name__ == '__main__':

    GAME_FIELD = pygame.display.set_mode(
        (GAME_FIELD_WIDTH, GAME_FIELD_HEIGHT)
    )
    config_path = '../data/neat_config_files/config_feedforward.txt'

    flappy_neat = FlappyNeat(config_path, score_threshold=1e3)
    winner = flappy_neat.get_winner()

    main(winner)
