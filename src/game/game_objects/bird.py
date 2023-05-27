from typing import List, Optional
from itertools import cycle

import pygame

from game.game_objects.constants import PATHES_TO_BIRD_IMGS
from game.globals.constants import (
    GAME_FIELD_HEIGHT, GAME_FIELD_WIDTH
)


class Bird:

    __x: int = int(0.2 * GAME_FIELD_WIDTH)
    __y: int = int(0.25 * GAME_FIELD_HEIGHT)
    __rotation: float = 0.
    __rotation_max: float = 30
    __rotation_min: float = -80

    __velocity: float = 0.
    __velocity_flap: float = -8
    __rotation_velocity: float = 10.

    __acceleration: float = 3
    __time_from_last_flap: float = 0.

    __displacement_thresh: float = 15.

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

        self.__time_from_last_flap += 1

        delta = self.__time_from_last_flap * self.__velocity
        delta += 0.5 * self.__acceleration * self.__time_from_last_flap ** 2

        delta = min(delta, self.__displacement_thresh)

        previous_position = self.__y
        self.__y = max(self.__y + delta, 0)

        if self.__y < previous_position:
            self.__rotation = self.__rotation_max

        else:
            self.__rotation = max(
                self.__rotation - self.__rotation_velocity,
                self.__rotation_min
            )

    def flap(self) -> None:
        self.__time_from_last_flap = 0
        self.__velocity = self.__velocity_flap

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
