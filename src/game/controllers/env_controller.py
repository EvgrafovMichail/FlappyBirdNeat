from typing import List

import pygame

from game.game_objects import PipesPair, Floor, Bird
from game.globals.constants import GAME_FIELD_WIDTH
from game.globals.enumerations import Scores
from game.globals.schemas import Position


class EnvController:

    __nearest_pipe_id: int = 0
    __pipes: List[PipesPair]
    __floor: Floor

    __distance_between_pipes: int = 180

    def __init__(self) -> None:
        self.__pipes = [PipesPair()]
        self.__floor = Floor()

    def move(self) -> None:

        pipe_to_remove = None

        for pipe in self.__pipes:

            pipe.move()

            distance_to_new_pipe = GAME_FIELD_WIDTH - pipe.position.x_left_pos

            if distance_to_new_pipe == self.__distance_between_pipes:
                self.__pipes.append(PipesPair())

            if pipe.position.x_right_pos < 0:
                pipe_to_remove = pipe

        if pipe_to_remove:
            self.__pipes.remove(pipe_to_remove)
            self.__nearest_pipe_id = 0

        self.__floor.move()

    def get_score(self, bird: Bird) -> float:

        if self.__is_collided(bird):
            return Scores.DIED.value

        if self.__is_pipe_passed(bird):
            return Scores.PIPE_PASSED.value

        return Scores.STILL_ALIVE.value

    def draw(self, window: pygame.Surface) -> None:

        for pipe in self.__pipes:
            pipe.draw(window)

        self.__floor.draw(window)

    def __is_collided(self, bird: Bird) -> bool:

        mask_bird = bird.mask
        pos_bird = bird.position

        for pipe in self.__pipes:

            mask_pipe_top, mask_pipe_bttm = pipe.mask
            pos_pipe = pipe.position

            offset_top = (pos_pipe.x_left_pos - pos_bird.x_left_pos,
                          pos_pipe.y_top_pos - int(pos_bird.y_top_pos))

            offset_bottom = (pos_pipe.x_left_pos - pos_bird.x_left_pos,
                             pos_pipe.y_bottom_pos - int(pos_bird.y_bottom_pos))

            collision_top = mask_bird.overlap(mask_pipe_top, offset_top)
            collision_bottom = mask_bird.overlap(mask_pipe_bttm, offset_bottom)

            if collision_top or collision_bottom:
                return True

        if pos_bird.y_bottom_pos >= self.__floor.position.y_top_pos:
            return True

        return False

    def __is_pipe_passed(self, bird: Bird) -> bool:

        nearest_pipe_id_prev = self.__nearest_pipe_id

        if len(self.__pipes) > 1:
            if self.__pipes[0].position.x_right_pos < bird.position.x_left_pos:
                self.__nearest_pipe_id = 1

        return nearest_pipe_id_prev != self.__nearest_pipe_id
    
    @property
    def nearest_pipe_position(self) -> Position:
        return self.__pipes[self.__nearest_pipe_id].position
