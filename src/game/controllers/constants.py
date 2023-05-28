import os


BG_IMAGE_PATH = os.path.join('..', 'data', 'sprites', 'background.png')

PATH_TO_DIGIT_FOLDER = os.path.join('..', 'data', 'sprites', 'digits')
PATHES_TO_DIGIT_IMGS = [
    os.path.join(PATH_TO_DIGIT_FOLDER, f'{i}.png')
    for i in range(10)
]
