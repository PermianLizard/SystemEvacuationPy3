import logging

import pyglet
from game import asteroid
from game import base
from game import collision
from game import const
from game import font
from game import level
from game import map_scene
from game import phys
from game import planet
from game import player
from game import render
from game import ship
from plib import ecs
from plib import scene
from plib.director import director
from pyglet import gl


class GameEcsManager(ecs.EcsManager):
    def __init__(self):
        super(GameEcsManager, self).__init__()

        # systems
        self.add_system(phys.PhysicsEcsSystem())
        self.add_system(collision.CollisionEcsSystem())
        self.add_system(ship.ShipEcsSystem())
        self.add_system(base.BaseEcsSystem())
        self.add_system(asteroid.AsteroidEcsSystem())
        self.add_system(player.PlayerEscSystem())
        self.add_system(render.RenderAnimationEcsSystem())

        # renderers
        self.add_renderer(render.GameEcsRenderer())

        # input handlers
        self.add_input_handler(player.PlayerEscInputHandler())

        # register components
        self.reg_comp_type(phys.PhysicsEcsComponent.name())
        self.reg_comp_type(phys.GravityEcsComponent.name())
        self.reg_comp_type(collision.CollisionEcsComponent.name())
        self.reg_comp_type(player.PlayerIdentityEcsComponent.name())
        self.reg_comp_type(planet.PlanetEcsComponent.name())
        self.reg_comp_type(ship.ShipEcsComponent.name())
        self.reg_comp_type(base.BaseEcsComponent.name())
        self.reg_comp_type(asteroid.AsteroidEcsComponent.name())
        self.reg_comp_type(planet.RenderPlanetEcsComponent.name())
        self.reg_comp_type(ship.RenderShipEcsComponent.name())
        self.reg_comp_type(base.RenderBaseEcsComponent.name())
        self.reg_comp_type(asteroid.RenderAsteroidEcsComponent.name())
        self.reg_comp_type(render.RenderAnimationEcsComponent.name())

    def init(self):
        level.generate_system(ecsm)

        super(GameEcsManager, self).init()

        self.victory = False
        self.defeat = False
        self.defeat_event = ''

        self._entities_to_remove = set()
        self._navigation = True

    def crew_rescued(self, eid, amount):
        self.dispatch_event('on_crew_rescued', eid, amount)

    def declare_victory(self, system_name, event):
        self.victory = True

    def declare_defeat(self, system_name, event):
        print('player bit it!')
        self.defeat = True
        self.defeat_event = event

    def entity_collision(self, e1id, e2id, impact_size, e1reflect, system_name, event):
        self.dispatch_event('on_entity_collision', e1id, e2id, impact_size, e1reflect, system_name, event)

    def mark_entity_for_removal(self, eid):
        self._entities_to_remove.add(eid)

    def kill_entity(self, eid, system_name='', event=''):
        self.dispatch_event('on_entity_kill', eid, system_name, event)
        self.mark_entity_for_removal(eid)

    def update(self, dt):
        self._entities_to_remove = set()

        super(GameEcsManager, self).update(dt)

        for eid in self._entities_to_remove:
            self.remove_entity(eid)


GameEcsManager.register_event_type('on_entity_collision')
GameEcsManager.register_event_type('on_entity_kill')
GameEcsManager.register_event_type('on_crew_rescued')

game_scene = None
ecsm = None


def init():
    global game_scene
    game_scene = GameScene()


def new_game():
    logging.debug('new game started')
    global ecsm
    ecsm = GameEcsManager()
    ecsm.keys = director.keys
    ecsm.setup_handlers()
    ecsm.init()


def clean_game():
    global ecsm
    ecsm.cleanup()
    ecsm.keys = None
    ecsm = None


class GameScene(scene.Scene):
    def __init__(self):
        super(GameScene, self).__init__()

    def enter(self):
        new_game()
        self.paused = True
        self.victory = False
        self.defeat = False

        self.title_label = pyglet.text.Label('Start',
                                             font_name=font.FONT_MONO.name,
                                             font_size=40,
                                             width=const.WIDTH - 200,
                                             x=const.WIDTH // 2, y=(const.HEIGHT // 2) + 100,
                                             anchor_x='center', anchor_y='center', multiline=True,
                                             color=(255, 255, 255, 255))

        self.text_label = pyglet.text.Label('',
                                            font_name=font.FONT_MONO.name,
                                            font_size=18,
                                            width=const.WIDTH - 200,
                                            x=const.WIDTH // 2, y=const.HEIGHT // 2,
                                            anchor_x='center', anchor_y='center', multiline=True,
                                            color=(255, 255, 255, 255))

        self.control_label = pyglet.text.Label('Press <P> to Begin',
                                               font_name=font.FONT_MONO.name,
                                               font_size=18,
                                               width=const.WIDTH - 200,
                                               x=const.WIDTH // 2, y=(const.HEIGHT // 2) - 200,
                                               anchor_x='center', anchor_y='center', multiline=True,
                                               color=(255, 255, 255, 255))

    def exit(self):
        clean_game()

    def draw(self):
        ecsm.draw()

        if self.paused or self.victory or self.defeat:
            gl.glColor4f(.2, .2, .2, .4)
            gl.glBegin(gl.GL_QUADS)
            gl.glVertex2f(0, 0)
            gl.glVertex2f(const.WIDTH, 0)
            gl.glVertex2f(const.WIDTH, const.HEIGHT)
            gl.glVertex2f(0, const.HEIGHT)
            gl.glEnd()

            self.title_label.draw()
            self.text_label.draw()
            self.control_label.draw()

    def update(self, dt):
        if ecsm and not self.paused and not self.victory:
            ecsm.update(dt)
            if ecsm.victory:
                self.victory = True
                self.title_label.text = 'VICTORY!'
                self.control_label.text = 'Press <ESC> to  Continue'
            if ecsm.defeat:
                self.defeat = True
                self.title_label.text = 'You\'ve botched it!'
                self.control_label.text = 'Press <ESC> to  Continue'

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            director.pop()

        if not self.victory and not self.defeat:
            if symbol == pyglet.window.key.P:
                self.paused = not self.paused
                if self.paused:
                    self.title_label.text = 'PAUSED'
                    self.control_label.text = 'Press <P> to Unpause'

        if not self.paused and not self.victory and not self.defeat:
            if symbol == pyglet.window.key.TAB:
                director.push(map_scene.map_scene)
            elif symbol == pyglet.window.key.N and ecsm:
                ecsm._navigation = not ecsm._navigation
            elif not self.paused and ecsm:
                ecsm.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        if not self.paused and not self.victory and not self.defeat:
            ecsm.on_key_release(symbol, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.paused and not self.victory and not self.defeat:
            ecsm.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.paused and not self.victory and not self.defeat:
            ecsm.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        if not self.paused and not self.victory and not self.defeat:
            ecsm.on_mouse_release(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not self.paused and not self.victory and not self.defeat:
            ecsm.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_enter(self, x, y):
        if not self.paused and not self.victory and not self.defeat:
            ecsm.on_mouse_enter(x, y)

    def on_mouse_leave(self, x, y):
        if not self.paused and not self.victory and not self.defeat:
            ecsm.on_mouse_leave(x, y)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if not self.paused and not self.victory and not self.defeat:
            ecsm.on_mouse_scroll(x, y, scroll_x, scroll_y)
