from typing import List

import pygame

from game.controllers.constants import PATHES_TO_DIGIT_IMGS
from game.globals.constants import (
    GAME_FIELD_WIDTH, GAME_FIELD_HEIGHT
)


class ScoreController:

    __images: List[pygame.Surface]

    def __init__(self) -> None:

        self.__images = [
            pygame.image.load(path_to_image).convert_alpha()
            for path_to_image in PATHES_TO_DIGIT_IMGS
        ]

    def draw(self, window: pygame.Surface, score: int) -> None:

        if score < 10:
            digits = [int(score)]

        else:
            digits = list(map(int, list(str(score))))

        width_total = 0

        for digit in digits:
            width_total += self.__images[digit].get_width()

        offset_x = (GAME_FIELD_WIDTH - width_total) / 2

        for digit in digits:
            window.blit(
                self.__images[digit],
                (offset_x, GAME_FIELD_HEIGHT * 0.1)
            )
            offset_x += self.__images[digit].get_width()
