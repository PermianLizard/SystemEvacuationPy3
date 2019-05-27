import plib.scene
import pyglet
from game import const
from game import font
from game import game_scene
from game import instruct
from game import starfield
from plib.director import director

menu_scene = None


def init():
    global menu_scene
    menu_scene = MenuScene()


class MenuScene(plib.scene.Scene):
    def __init__(self):
        super(MenuScene, self).__init__()

        self.menu_label = pyglet.text.Label('SYSTEM EVACUATION',
                                            font_name=font.FONT_MONO.name,
                                            font_size=32,
                                            x=20, y=const.HEIGHT - 10,
                                            anchor_x='left', anchor_y='top',
                                            color=(255, 255, 255, 255))

        self.options_label = pyglet.text.Label('<S> Start Game\n<I> Instructions\n<X> Exit',
                                               font_name=font.FONT_MONO.name,
                                               font_size=18,
                                               multiline=True,
                                               width=400,
                                               x=20, y=const.HEIGHT - 100,
                                               anchor_x='left', anchor_y='top',
                                               color=(255, 255, 255, 255))

        self.starfield = starfield.Starfield((0, 0, const.WIDTH, const.HEIGHT), 400)
        self.ty = 0

    def update(self, dt):
        self.ty -= 1

    def draw(self):
        self.starfield.draw(0, self.ty)

        self.menu_label.draw()
        self.options_label.draw()

    def on_key_press(self, symbol, modifiers):
        super(MenuScene, self).on_key_press(symbol, modifiers)

        if symbol == pyglet.window.key.S:
            director.push(game_scene.game_scene)
        if symbol == pyglet.window.key.I:
            director.push(instruct.instruct_scene)
        if symbol == pyglet.window.key.X:
            director.pop()
