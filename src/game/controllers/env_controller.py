from typing import List

import pygame

from game.game_objects import PipesPair, Floor, Bird
from game.globals.constants import GAME_FIELD_WIDTH

class EnvController:

    __pipes: List[PipesPair]
    __floor: Floor

    __distance_between_pipes: int = 165

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

        self.__floor.move()

    def get_score(self, bird: Bird) -> float:

        if self.__is_collided(bird):
            return -1000
        
        if self.__is_pipe_passed(bird):
            return 1
        
        return 0.01

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

        nearest_pipe_id = 0

        if len(self.__pipes) > 1:
            if self.__pipes[0].position.x_left_pos < bird.position.x_left_pos:
                nearest_pipe_id = 1

        pipes_center_pos = self.__pipes[nearest_pipe_id].position.x_left_pos
        pipes_center_pos += self.__pipes[nearest_pipe_id].position.x_right_pos
        pipes_center_pos /= 2

        return pipes_center_pos < bird.position.x_left_pos
