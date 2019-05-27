import pyglet
from game import base
from game import collision
from game import const
from game import font
from game import game_scene
from game import phys
from game import planet
from game import player
from game import render
from game import ship
from plib import scene
from plib.director import director
from pyglet import gl
map_scene = None

ZOOM = 0.040
TOKEN_SIZE = 50


def init():
    global map_scene
    map_scene = MapScene()


class MapScene(scene.Scene):
    def __init__(self):
        super(MapScene, self).__init__()

    def enter(self):
        pass

    def exit(self):
        pass

    def draw(self):
        gl.glLineWidth(1)

        ecsm = game_scene.ecsm

        phys_comp_list = ecsm.comps[phys.PhysicsEcsComponent.name()]
        grav_comp_list = ecsm.comps[phys.GravityEcsComponent.name()]
        coll_comp_list = ecsm.comps[collision.CollisionEcsComponent.name()]
        planet_comp_list = ecsm.comps[planet.PlanetEcsComponent.name()]
        ship_comp_list = ecsm.comps[ship.ShipEcsComponent.name()]
        base_comp_list = ecsm.comps[base.BaseEcsComponent.name()]

        entities = ecsm.entities

        player_entity_id = ecsm.get_system(player.PlayerEscSystem.name()).player_entity_id
        player_physc = ecsm.get_entity_comp(player_entity_id, phys.PhysicsEcsComponent.name())

        # if player_physc:
        #	tx = (-player_physc.pos.x * ZOOM) + const.WIDTH // 2
        #	ty = (-player_physc.pos.y * ZOOM) + const.HEIGHT // 2
        # else:
        tx = const.WIDTH // 2
        ty = const.HEIGHT // 2

        gl.glColor3f(0, 0, 0.2)
        for i in range(0, const.WIDTH, 50):
            gl.glBegin(gl.GL_LINES)
            gl.glVertex2f(i, 0.0)
            gl.glVertex2f(i, const.HEIGHT)
            gl.glEnd()

        for i in range(0, const.HEIGHT, 50):
            gl.glBegin(gl.GL_LINES)
            gl.glVertex2f(0.0, i)
            gl.glVertex2f(const.WIDTH, i)
            gl.glEnd()

        gl.glPushMatrix()
        gl.glLoadIdentity()

        gl.glTranslatef(tx, ty, 0.0)

        # planet orbots
        for idx, eid in enumerate(entities):
            planetc = planet_comp_list[idx]
            physc = phys_comp_list[idx]

            if planetc and physc.static:
                # rpc = rend_plan_comp_list[idx]
                # render.draw_circle(physc.pos.x * ZOOM, physc.pos.y * ZOOM, collc.radius * ZOOM)

                distance = physc.pos.length
                if distance:
                    render.draw_circle(0, 0, distance * ZOOM, mode=gl.GL_LINES, color=(.5, .5, .5, 1))

        for idx, eid in enumerate(entities):
            shipc = ship_comp_list[idx]
            basec = base_comp_list[idx]
            planetc = planet_comp_list[idx]
            physc = phys_comp_list[idx]
            collc = coll_comp_list[idx]

            if basec and basec.crew_load > 0:
                render.draw_circle(physc.pos.x * ZOOM, physc.pos.y * ZOOM, TOKEN_SIZE * ZOOM, color=(1, 1, 0, 1))

            # show planet
            elif planetc:
                # rpc = rend_plan_comp_list[idx]
                render.draw_circle(physc.pos.x * ZOOM, physc.pos.y * ZOOM, collc.radius * ZOOM, color=(.8, .8, .8, 1))

                # gc = grav_comp_list[idx]
                # if gc and gc.gravity_radius:
            #	render.draw_circle(physc.pos.x * ZOOM, physc.pos.y * ZOOM, gc.gravity_radius * ZOOM, None, gl.GL_LINE_LOOP, color=(.3, .3, .3, 1))

        # labels
        for idx, eid in enumerate(entities):
            planetc = planet_comp_list[idx]
            physc = phys_comp_list[idx]
            collc = coll_comp_list[idx]

            if planetc:
                if planetc.pname:
                    label = pyglet.text.Label(planetc.pname,
                                              font_name=font.FONT_MONO.name,
                                              font_size=12,
                                              x=physc.pos.x * ZOOM, y=(physc.pos.y + (collc.radius + 500)) * ZOOM,
                                              # + collc.radius + 5
                                              anchor_x='center', anchor_y='center',
                                              color=(255, 255, 255, 120))
                    label.draw()

        # show player position
        if player_physc:
            render.draw_circle(player_physc.pos.x * ZOOM, player_physc.pos.y * ZOOM, TOKEN_SIZE * ZOOM,
                               color=(1, 0, 0, 1))

        gl.glPopMatrix()

    def update(self, dt):
        if not director.keys[pyglet.window.key.TAB]:
            director.pop()

    def on_key_press(self, symbol, modifiers):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass
