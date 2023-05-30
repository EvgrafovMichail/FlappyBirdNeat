from enum import Enum


class Scores(Enum):
    PIPE_PASSED = 1
    STILL_ALIVE = 0.01
    DIED = -1
