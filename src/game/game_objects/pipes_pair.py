from typing import List, Optional, Tuple
from random import choice

import pygame

from game.game_objects.constants import PATH_TO_PIPE_IMG
from game.game_objects.schemas import Position
from game.globals.constants import GAME_FIELD_WIDTH


class PipesPair:

    __x: int = GAME_FIELD_WIDTH
    __y_top: int = 0
    __y_bottom: int = 0

    __gap_size: int = 100
    __gaps: List[int] = [50 + i * 25 for i in range(2, 10)]

    __velocity: int = 5

    __top_pipe_img: pygame.Surface
    __bottom_pipe_img: pygame.Surface

    def __init__(self, x_pos: Optional[int] = None) -> None:

        if x_pos:
            self.__x = x_pos
        
        self.__bottom_pipe_img = pygame.image.load(PATH_TO_PIPE_IMG)
        self.__bottom_pipe_img = self.__bottom_pipe_img.convert_alpha()
        self.__top_pipe_img =  pygame.transform.flip(
            self.__bottom_pipe_img, False, True
        )

        y_gap = choice(self.__gaps)
        self.__y_top = y_gap - self.__top_pipe_img.get_height()
        self.__y_bottom = y_gap + self.__gap_size

    def move(self) -> None:
        self.__x -= self.__velocity

    def draw(self, window: pygame.Surface) -> None:

        top_pipe_pos = (self.__x, self.__y_top)
        bottom_pipe_pos = (self.__x, self.__y_bottom)

        window.blit(self.__top_pipe_img, top_pipe_pos)
        window.blit(self.__bottom_pipe_img, bottom_pipe_pos)

    @property
    def mask(self) -> Tuple[pygame.Mask, pygame.Mask]:

        mask_top = pygame.mask.from_surface(self.__top_pipe_img)
        mask_bottom = pygame.mask.from_surface(self.__bottom_pipe_img)

        return mask_top, mask_bottom

    @property
    def position(self) -> Position:

        position = Position(
            x_left_pos=self.__x,
            x_right_pos=self.__x + self.__top_pipe_img.get_width(),
            y_top_pos=self.__y_top,
            y_bottom_pos=self.__y_bottom
        )

        return position
