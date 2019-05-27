import math

import pyglet
from game import anim
from game import img
from game import phys
from game import planet
from game import render
from plib import ecs
from plib import vec2d


class ShipEcsComponent(ecs.EcsComponent):
    @classmethod
    def name(cls):
        return 'ship-component'

    def __init__(self, rotation=0.0, rotation_speed=0, thrust_force=0.0, impact_resistance=110.0, fuel=10000,
                 passengers=1, health=300):
        super(ShipEcsComponent, self).__init__()

        self.rotation = float(rotation)
        self.thrust_force = float(thrust_force)
        self.rotation_speed = float(rotation_speed)
        self.impact_resistance = float(impact_resistance)
        self.fuel_max = fuel
        self.fuel = fuel
        self.passengers = passengers
        self.health_max = health
        self.health = health

        self.messages = []

    def process(self):
        for message in self.messages:
            message[1] -= 1
            if message[1] == 0:
                self.messages.remove(message)
                print('removed message')

    def __str__(self):
        return 'ShipEcsComponent'


class RenderShipEcsComponent(ecs.EcsComponent):
    THRUST_COOLDOWN_TIME = 5

    @classmethod
    def name(cls):
        return 'render-ship-component'

    def __init__(self):
        super(RenderShipEcsComponent, self).__init__()

        self.spr = pyglet.sprite.Sprite(img.get(img.IMG_SHIP))
        self.thrust_spr = pyglet.sprite.Sprite(anim.get(anim.ANIM_THRUST))

        self.thrust_cooldown = 0

    def thrust_started(self):
        self.thrust_cooldown = RenderShipEcsComponent.THRUST_COOLDOWN_TIME

    def process(self):
        if self.thrust_cooldown:
            self.thrust_cooldown -= 1

    def __str__(self):
        return 'RenderShipEcsComponent'


class ShipEcsSystem(ecs.EcsSystem):
    @classmethod
    def name(cls):
        return 'ship-system'

    def __init__(self):
        super(ShipEcsSystem, self).__init__()

    def turn_left(self, eid):
        sc = self.manager.get_entity_comp(eid, ShipEcsComponent.name())
        sc.rotation += sc.rotation_speed

    def turn_right(self, eid):
        sc = self.manager.get_entity_comp(eid, ShipEcsComponent.name())
        sc.rotation -= sc.rotation_speed

    def thrust_forward(self, eid):
        sc = self.manager.get_entity_comp(eid, ShipEcsComponent.name())

        if sc.fuel > 0:
            rsc = self.manager.get_entity_comp(eid, RenderShipEcsComponent.name())
            pc = self.manager.get_entity_comp(eid, phys.PhysicsEcsComponent.name())

            if not sc or not pc: return

            dir_radians = math.radians(sc.rotation)
            dirv = vec2d.vec2d(math.cos(dir_radians), math.sin(dir_radians))
            dirv.length = sc.thrust_force

            sc.fuel -= 1

            pc.apply_force(dirv.x, dirv.y)

            rsc.thrust_started()
        else:
            print('out of fuel')

    def award_fuel(self, eid, amount):
        sc = self.manager.get_entity_comp(eid, ShipEcsComponent.name())
        pc = self.manager.get_entity_comp(eid, phys.PhysicsEcsComponent.name())
        print('ship refuel', amount)
        if sc.fuel < sc.fuel_max:
            sc.fuel += amount
            if sc.fuel > sc.fuel_max:
                sc.fuel = sc.fuel_max

            sc.messages.append(['+ %s FUEL' % amount, 80, pc.pos.x - 50, pc.pos.y + 50, (0, 255, 0, 255), None])

    def award_crew(self, eid, amount):
        sc = self.manager.get_entity_comp(eid, ShipEcsComponent.name())
        pc = self.manager.get_entity_comp(eid, phys.PhysicsEcsComponent.name())
        print('ship get crew', amount)

        sc.passengers += amount

        sc.messages.append(['+ %s CREW' % amount, 80, pc.pos.x - 50, pc.pos.y + 50, (0, 255, 0, 255), None])

        self.manager.crew_rescued(eid, amount)

    def award_health(self, eid, amount):
        sc = self.manager.get_entity_comp(eid, ShipEcsComponent.name())
        pc = self.manager.get_entity_comp(eid, phys.PhysicsEcsComponent.name())
        print('ship get health', amount)

        sc.health += amount

        sc.messages.append(['+ %s REPAIRED' % amount, 80, pc.pos.x - 50, pc.pos.y + 50, (0, 255, 0, 255), None])

    def receive_damage(self, eid, amount):
        sc = self.manager.get_entity_comp(eid, ShipEcsComponent.name())
        pc = self.manager.get_entity_comp(eid, phys.PhysicsEcsComponent.name())
        print('ship receive damage', amount)
        sc.health -= amount
        if sc.health < 0:
            sc.health = 0
            self.manager.kill_entity(eid)

    def on_entity_kill(self, eid, system_name, event):
        sc = self.manager.get_entity_comp(eid, ShipEcsComponent.name())
        pc = self.manager.get_entity_comp(eid, phys.PhysicsEcsComponent.name())
        if sc:
            self.manager.create_entity(
                comps=[render.RenderAnimationEcsComponent(pc.pos.x, pc.pos.y, anim.ANIM_SHIP_EXP)])

    def on_entity_collision(self, e1id, e2id, impact_size, e1reflect, system_name, event):
        e1sc = self.manager.get_entity_comp(e1id, ShipEcsComponent.name())
        if e1sc:
            if self.manager.get_entity_comp(e2id, planet.PlanetEcsComponent.name()):
                self.manager.kill_entity(e1id)
            elif impact_size > e1sc.impact_resistance:
                damage = int(impact_size - e1sc.impact_resistance)
                if damage > 0:
                    self.receive_damage(e1id, damage)
            else:
                e1pc = self.manager.get_entity_comp(e1id, phys.PhysicsEcsComponent.name())
                e1pc.vel += e1reflect

    def update(self, dt):
        ship_comp_list = self.manager.comps[ShipEcsComponent.name()]

        entities = self.manager.entities
        for idx, eid in enumerate(entities):
            shipc = ship_comp_list[idx]
            if shipc:
                shipc.process()
