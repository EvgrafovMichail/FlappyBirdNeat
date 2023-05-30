from typing import List, Optional
from itertools import cycle

import pygame

from game.game_objects.constants import PATHES_TO_BIRD_IMGS
from game.globals.schemas import Position
from game.globals.constants import (
    GAME_FIELD_HEIGHT, GAME_FIELD_WIDTH
)


class Bird:

    __x: int = int(0.2 * GAME_FIELD_WIDTH)
    __y: float = int(0.25 * GAME_FIELD_HEIGHT)
    __rotation: float = 0.
    __rotation_max: float = 25
    __rotation_min: float = -80

    __velocity: float = 0.
    __velocity_flap: float = -8
    __velocity_max: float = 10
    __rotation_velocity: float = 3.

    __acceleration: float = 1
    __is_flapped: bool = False

    __images: List[pygame.Surface]
    __image_id: int = 0
    __image_ids: cycle
    __img_loop_index: int = 0

    def __init__(
            self,
            pos_x: Optional[int] = None,
            pos_y: Optional[int] = None
        ) -> None:

        if pos_x:
            self.__x = pos_x

        if pos_y:
            self.__y = pos_y

        self.__images = [
            pygame.image.load(path_to_bird_image).convert_alpha()
            for path_to_bird_image in PATHES_TO_BIRD_IMGS
        ]
        self.__image_ids = cycle(list(range(len(self.__images))))

    def move(self) -> None:

        if self.__velocity < self.__velocity_max and not self.__is_flapped:
            self.__velocity += self.__acceleration

        if self.__is_flapped:
            self.__is_flapped = False

        previous_position = self.__y
        self.__y += self.__velocity

        self.__y = max(self.__y, 0)

        if self.__y < previous_position:
            self.__rotation = self.__rotation_max

        else:
            self.__rotation = max(
                self.__rotation - self.__rotation_velocity,
                self.__rotation_min
            )

    def flap(self) -> None:
        self.__velocity = self.__velocity_flap
        self.__is_flapped = True

    def draw(self, window: pygame.Surface) -> None:

        if self.__img_loop_index % 5 == 0:
            self.__image_id = next(self.__image_ids)

        if self.__rotation < 0:
            image_curr = self.__images[1]

        else:
            image_curr = self.__images[self.__image_id]

        self.__img_loop_index += 1

        image_rotated = pygame.transform.rotate(
            image_curr, self.__rotation
        )

        bird_pos = (self.__x, self.__y)
        image_rect = image_rotated.get_rect(
            center=image_curr.get_rect(topleft=bird_pos).center
        )

        window.blit(image_rotated, image_rect.topleft)

    @property
    def mask(self) -> pygame.Mask:
        return pygame.mask.from_surface(
            self.__images[self.__image_id]
        )

    @property
    def velocity(self) -> float:
        return self.__velocity

    @property
    def position(self) -> Position:

        img_curr = self.__images[self.__image_id]

        position = Position(
            x_left_pos=self.__x,
            y_top_pos=self.__y,
            y_bottom_pos=self.__y + img_curr.get_height()
        )

        return position
