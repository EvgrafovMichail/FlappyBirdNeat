import os

################################################################################
#                                PATHES TO IMAGES                              #
################################################################################

# path to background image
BG_IMAGE_PATH = os.path.join('..', 'data', 'sprites', 'background.png')

# pathes to digit images
PATH_TO_DIGIT_FOLDER = os.path.join('..', 'data', 'sprites', 'digits')
PATHES_TO_DIGIT_IMGS = [
    os.path.join(PATH_TO_DIGIT_FOLDER, f'{i}.png')
    for i in range(10)
]
