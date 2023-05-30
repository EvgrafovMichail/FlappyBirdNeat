from typing import Optional

from pydantic import BaseModel


class Position(BaseModel):
    x_left_pos: Optional[float] = None
    x_right_pos: Optional[float] = None
    y_top_pos: Optional[float] = None
    y_bottom_pos: Optional[float] = None