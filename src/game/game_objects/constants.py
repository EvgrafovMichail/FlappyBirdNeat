import os

from game.globals.constants import (
    GAME_FIELD_HEIGHT, GAME_FIELD_WIDTH
)

################################################################################
#                                PATHES TO IMAGES                              #
################################################################################

# pathes to images with bird
PATH_TO_BIRD_FOLDER = os.path.join('..', 'data', 'sprites', 'bird')
PATHES_TO_BIRD_IMGS = [
    os.path.join(PATH_TO_BIRD_FOLDER, 'downflap.png'),
    os.path.join(PATH_TO_BIRD_FOLDER, 'midflap.png'),
    os.path.join(PATH_TO_BIRD_FOLDER, 'upflap.png')
]

# path to pipe image
PATH_TO_PIPE_IMG = os.path.join('..', 'data','sprites', 'pipe.png')

# path to floor image
PATH_TO_FLOOR_IMG = os.path.join('..', 'data', 'sprites', 'base.png')


################################################################################
#                                BIRD CONSTANTS                                #
################################################################################

BIRD_X_DEFAULT = int(0.2 * GAME_FIELD_WIDTH)
BIRD_Y_DEFAULT = int(0.75 * GAME_FIELD_HEIGHT)
