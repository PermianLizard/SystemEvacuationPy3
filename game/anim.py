import os

import pyglet
from game import start

ANIM_THRUST = 'thrust.png'
ANIM_SHIP_EXP = 'ship_exp.png'

anim_name_list = [ANIM_THRUST, ANIM_SHIP_EXP]
anim_center_list = [True, True]
anim_frame_list = [3, 6]
anim_speed_list = [0.1, 0.1]
anim_dict = {}

anim_bin = pyglet.image.atlas.TextureBin()


def init():
    PATH = os.path.join(start.DATA_PATH, 'images')

    for idx, anim_name in enumerate(anim_name_list):
        img = pyglet.image.load(os.path.join(PATH, anim_name))
        img_grid = pyglet.image.ImageGrid(img, 1, anim_frame_list[idx])
        anim = pyglet.image.Animation.from_image_sequence(img_grid, anim_speed_list[idx], True)

        anim.add_to_texture_bin(anim_bin)

        if anim_center_list[idx]:
            for f in anim.frames:
                f.image.anchor_x = f.image.width // 2
                f.image.anchor_y = f.image.height // 2

        anim_dict[anim_name] = anim


def get(name):
    return anim_dict[name]
