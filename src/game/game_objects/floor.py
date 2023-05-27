from typing import Optional

import pygame

from game.game_objects.constants import PATH_TO_FLOOR_IMG
from game.globals.constants import (
    GAME_FIELD_HEIGHT, GAME_FIELD_WIDTH
)


class Floor:

    __y: int = int(0.9 * GAME_FIELD_HEIGHT)
    __x1: int = 0
    __x2: int = GAME_FIELD_WIDTH
    __width: int = GAME_FIELD_WIDTH

    __velocity: int = 5

    __image: pygame.Surface

    def __init__(self, y_pos: Optional[int] = None) -> None:

        if y_pos:
            self.__y = y_pos

        self.__image = pygame.image.load(PATH_TO_FLOOR_IMG)
        self.__image = self.__image.convert_alpha()

    def move(self) -> None:

        self.__x1 -= self.__velocity
        self.__x2 -= self.__velocity

        if self.__x1 + self.__width <= 0:
            self.__x1 = self.__x2 + self.__width

        if self.__x2 + self.__width <= 0:
            self.__x2 = self.__x1 + self.__width

    def draw(self, window: pygame.Surface) -> None:

        floor_seg1_pos = (self.__x1, self.__y)
        floor_seg2_pos = (self.__x2, self.__y)

        window.blit(self.__image, floor_seg1_pos)
        window.blit(self.__image, floor_seg2_pos)

    @property
    def level(self) -> int:
        return self.__y
