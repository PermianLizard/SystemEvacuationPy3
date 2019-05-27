import plib.scene
import pyglet
from game import const
from game import font
from game import starfield
from plib.director import director

instruct_scene = None


def init():
    global instruct_scene
    instruct_scene = InstructScene()


class InstructScene(plib.scene.Scene):
    def __init__(self):
        super(InstructScene, self).__init__()

        self.menu_label = pyglet.text.Label('Instructions',
                                            font_name=font.FONT_MONO.name,
                                            font_size=32,
                                            x=20, y=const.HEIGHT - 10,
                                            anchor_x='left', anchor_y='top',
                                            color=(255, 255, 255, 255))

        self.options_label = pyglet.text.Label('''Well It\'s all gone to shit.
Not two days into our survey of this toilet of a system a swarm of asteroids decides hit us. With that kind of welcome, we'll be getting right back out of here.

Problem is, the fist wave of rocks wiped out all but one of our ships and we've still got most of our crew stationed out there.
We need you to make good on our one remaining ship. You must navigate this minefield and rescue our people. 

Just remember, we've got limited time. Our scans show us that the next wave of asteroids is going to put us all through the shredder. Not only that but you'll have limited fuel for this mission.
With any luck our bases should be able to top you up and do some repairs as well.

Don't forget you have a handy navigation map you can use to survey the whole mess. Press and hold <TAB> to bring it up -good luck!
''',
                                               font_name=font.FONT_MONO.name,
                                               font_size=10,
                                               multiline=True,
                                               width=const.WIDTH - 100,
                                               x=20, y=const.HEIGHT - 100,
                                               anchor_x='left', anchor_y='top',
                                               color=(255, 255, 255, 255))

        self.starfield = starfield.Starfield((0, 0, const.WIDTH, const.HEIGHT), 400)
        self.ty = 0

    def draw(self):
        self.ty -= 1
        self.starfield.draw(0, self.ty)

        self.menu_label.draw()
        self.options_label.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            director.pop()
