import random

import pyglet
from game import anim
from game import collision
from game import const
from game import img
from game import phys
from game import planet
from game import player
from game import render
from game import ship
from plib import ecs
from plib import vec2d

POSITION_ANGLES = [i for i in range(0, 360, 20)]


class AsteroidEcsComponent(ecs.EcsComponent):
    @classmethod
    def name(cls):
        return 'asteroid-component'

    def __init__(self, impact_resistance=110.0, health=300):
        super(AsteroidEcsComponent, self).__init__()

        self.impact_resistance = float(impact_resistance)
        self.health_max = health
        self.health = health

    def __str__(self):
        return 'AsteroidEcsComponent'


class RenderAsteroidEcsComponent(ecs.EcsComponent):
    @classmethod
    def name(cls):
        return 'render-asteroid-component'

    def __init__(self, img_name=''):
        super(RenderAsteroidEcsComponent, self).__init__()

        if img_name:
            self.spr = pyglet.sprite.Sprite(img.get(img_name))
        else:
            self.spr = None

    def __str__(self):
        return 'RenderAsteroidEcsComponent'


class AsteroidEcsSystem(ecs.EcsSystem):
    @classmethod
    def name(cls):
        return 'asteroid-system'

    def __init__(self):
        super(AsteroidEcsSystem, self).__init__()

        self.generate_radius = const.WIDTH + 20

    def receive_damage(self, eid, amount):
        ac = self.manager.get_entity_comp(eid, AsteroidEcsComponent.name())
        print('asteroid receive damage', amount)
        ac.health -= amount
        if ac.health < 0:
            ac.health = 0
            self.manager.kill_entity(eid)

    def on_entity_collision(self, e1id, e2id, impact_size, e1reflect, system_name, event):
        e1ac = self.manager.get_entity_comp(e1id, AsteroidEcsComponent.name())
        if e1ac:
            if self.manager.get_entity_comp(e2id, planet.PlanetEcsComponent.name()):
                self.manager.kill_entity(e1id)
            elif impact_size > e1ac.impact_resistance:
                damage = int(impact_size - e1ac.impact_resistance)
                if damage > 0:
                    self.receive_damage(e1id, damage)
            else:
                e1pc = self.manager.get_entity_comp(e1id, phys.PhysicsEcsComponent.name())
                e1pc.vel += e1reflect

    def on_entity_kill(self, eid, system_name, event):
        pass

    def on_entity_kill(self, eid, system_name, event):
        ac = self.manager.get_entity_comp(eid, AsteroidEcsComponent.name())
        pc = self.manager.get_entity_comp(eid, phys.PhysicsEcsComponent.name())
        if ac:
            self.manager.create_entity(
                comps=[render.RenderAnimationEcsComponent(pc.pos.x, pc.pos.y, anim.ANIM_SHIP_EXP)])

    def update(self, dt):
        player_sys = self.manager.get_system(player.PlayerEscSystem.name())

        phys_comp_list = self.manager.comps[phys.PhysicsEcsComponent.name()]
        coll_comp_list = self.manager.comps[collision.CollisionEcsComponent.name()]
        aster_comp_list = self.manager.comps[AsteroidEcsComponent.name()]

        # generate
        if player_sys.player_entity_id:
            player_pc = self.manager.get_entity_comp(player_sys.player_entity_id, phys.PhysicsEcsComponent.name())
            player_sc = self.manager.get_entity_comp(player_sys.player_entity_id, ship.ShipEcsComponent.name())
            if player_pc and player_sc:
                time = player_sys.time_limit
                if time % 20 == 0:

                    if player_pc.vel.length > random.randint(1, phys.SPEED_LIMIT):

                        player_angle = player_pc.vel.get_angle()
                        gen_angle = random.choice(
                            [angle for angle in range(int(player_angle - 90), int(player_angle + 90))])
                        gen_pos = vec2d.vec2d(self.generate_radius, 0)
                        gen_pos.rotate(gen_angle)
                        gen_pos = player_pc.pos + gen_pos

                        valid_pos = True
                        for idx, physc in enumerate(phys_comp_list):
                            if physc:
                                collc = coll_comp_list[idx]
                                if physc.pos.get_distance(gen_pos) < collc.radius:
                                    valid_pos = False

                        gen_vel = vec2d.vec2d(random.randint(0, 80), random.randint(0, 80))
                        # create new asteroid
                        if valid_pos:
                            self.manager.create_entity([phys.PhysicsEcsComponent(gen_pos.x, gen_pos.y, mass=100,
                                                                                 static=False, vx=gen_vel.x,
                                                                                 vy=gen_vel.y),
                                                        collision.CollisionEcsComponent(radius=14),
                                                        AsteroidEcsComponent(impact_resistance=50.0, health=100),
                                                        RenderAsteroidEcsComponent(img.IMG_ASTER)])

            entities = self.manager.entities
            for idx, eid in enumerate(entities):
                asterc = aster_comp_list[idx]
                if asterc:
                    physc = phys_comp_list[idx]
                    if physc and player_pc:
                        if player_pc.pos.get_distance(physc.pos) > self.generate_radius:
                            self.manager.mark_entity_for_removal(eid)
