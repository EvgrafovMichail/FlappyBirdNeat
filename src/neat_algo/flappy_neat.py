from typing import Optional, Any

import pygame
import neat
import os

from game.controllers import EnvController
from game.game_objects import Bird


class FlappyNeat:

    __config: Any
    __gen_num: int = 50
    __population: neat.Population
    __score_thresh: int = 175
    __winner: Optional[neat.nn.FeedForwardNetwork] = None

    def __init__(
            self,
            path_to_config: str,
            gen_num: int = 50,
            score_threshold: int = 175
        ) -> None:
        
        self.__config = neat.config.Config(
            neat.DefaultGenome, neat.DefaultReproduction,
            neat.DefaultSpeciesSet, neat.DefaultStagnation,
            path_to_config
        )

        if gen_num < 1:
            message = f'invalid gen_num value: {gen_num}; '
            message += 'natural number was expected;'
            raise ValueError(message)
        
        if score_threshold < 1:
            message = f'invalid score_threshold value: {gen_num}; '
            message += 'natural number was expected;'
            raise ValueError(message)

        self.__gen_num = gen_num
        self.__score_thresh = score_threshold
        self.__population = neat.Population(self.__config)

    def get_winner(self, verbose: bool = True) -> neat.nn.FeedForwardNetwork:

        if self.__winner:
            return self.__winner

        if verbose:
            self.__population.add_reporter(neat.StdOutReporter(True))
            stats = neat.StatisticsReporter()
            self.__population.add_reporter(stats)

        winner_genome = self.__population.run(
            self.__evaluate_fitness, self.__gen_num
        )

        self.__winner = neat.nn.FeedForwardNetwork.create(
            winner_genome, self.__config
        )

        return self.__winner

    def __evaluate_fitness(self, genomes, config) -> None:

        networks, birds, genes = [], [], []
        env_controller = EnvController()
        score_global = 0

        for _, genome in genomes:
            genome.fitness = 0

            networks.append(
                neat.nn.FeedForwardNetwork.create(genome, config)
            )
            birds.append(Bird())
            genes.append(genome)

        while 0 < len(birds) and score_global < self.__score_thresh:

            is_pipe_passed = False
            env_controller.move()

            for bird in birds:

                bird.move()

                output = networks[birds.index(bird)].activate((
                    bird.position.y_top_pos,
                    env_controller.neares_pipe_position.x_right_pos - bird.position.x_left_pos,
                    env_controller.neares_pipe_position.y_top_pos - bird.position.y_top_pos,
                    env_controller.neares_pipe_position.y_bottom_pos - bird.position.y_top_pos
                ))[0]

                if output > 0.5:
                    bird.flap()

                score = env_controller.get_score(bird)
                genes[birds.index(bird)].fitness += score

                if score == -1:
                    networks.pop(birds.index(bird))
                    genes.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

                elif score == 1:
                    is_pipe_passed = True

            if is_pipe_passed:
                score_global += 1
