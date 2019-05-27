import os

import pyglet
from game import start

IMG_SHIP = 'ship.png'
IMG_THRUST = 'thrust.png'
IMG_SUN = 'sun.png'
IMG_ASTER = 'aster.png'
IMG_P_64_1 = 'p64_1.png'
IMG_P_64_2 = 'p64_2.png'
IMG_M_48_1 = 'm48_1.png'
IMG_BASE = 'base.png'

img_name_list = [IMG_SHIP, IMG_THRUST, IMG_SUN, IMG_ASTER, IMG_P_64_1, IMG_P_64_2, IMG_M_48_1, IMG_BASE]
img_center_list = [True, True, True, True, True, True, True, True]
img_dict = {}


def init():
    PATH = os.path.join(start.DATA_PATH, 'images')

    for idx, img_name in enumerate(img_name_list):
        img = pyglet.image.load(os.path.join(PATH, img_name))
        if img_center_list[idx]:
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 2
        img_dict[img_name] = img


def get(name):
    return img_dict[name]
