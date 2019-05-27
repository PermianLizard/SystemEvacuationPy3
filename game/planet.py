import pyglet
from game import img
from plib import ecs


class PlanetEcsComponent(ecs.EcsComponent):
    @classmethod
    def name(cls):
        return 'planet-component'

    def __init__(self, pname):
        super(PlanetEcsComponent, self).__init__()
        self.pname = pname

    def __str__(self):
        return 'PlanetEcsComponent'


class RenderPlanetEcsComponent(ecs.EcsComponent):
    @classmethod
    def name(cls):
        return 'render-planet-component'

    def __init__(self, img_name=''):
        super(RenderPlanetEcsComponent, self).__init__()

        if img_name:
            print('img name: ', img_name)
            self.spr = pyglet.sprite.Sprite(img.get(img_name))
        else:
            self.spr = None

    def __str__(self):
        return 'RenderPlanetEcsComponent'
