from game import anim
from game import end_scene
from game import font
from game import game_scene
from game import img
from game import instruct
from game import map_scene
from game import menu_scene
from plib import director


def init():
    font.init()
    img.init()
    anim.init()
    menu_scene.init()
    instruct.init()
    game_scene.init()
    map_scene.init()
    end_scene.init()
    director.director.push(menu_scene.menu_scene)


def cleanup():
    pass
