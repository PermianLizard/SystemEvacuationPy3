import pyglet
from game import collision
from game import img
from game import phys
from game import planet
from game import ship
from plib import ecs


class BaseEcsComponent(ecs.EcsComponent):
    @classmethod
    def name(cls):
        return 'base-component'

    def __init__(self, radius, fuel_load=True, crew_load=True, repairs=True, impact_resistance=110.0, health=300):
        super(BaseEcsComponent, self).__init__()

        self.radius = float(radius)
        self.fuel_load = fuel_load
        self.crew_load = crew_load
        self.repairs = repairs

        self.impact_resistance = float(impact_resistance)
        self.health_max = health
        self.health = health

    def __str__(self):
        return 'BaseEcsComponent'


class RenderBaseEcsComponent(ecs.EcsComponent):
    @classmethod
    def name(cls):
        return 'render-base-component'

    def __init__(self, img_name=''):
        super(RenderBaseEcsComponent, self).__init__()

        if img_name:
            self.spr = pyglet.sprite.Sprite(img.get(img_name))
        else:
            self.spr = None

    def __str__(self):
        return 'RenderBaseEcsComponent'


class BaseEcsSystem(ecs.EcsSystem):
    @classmethod
    def name(cls):
        return 'base-system'

    def __init__(self):
        super(BaseEcsSystem, self).__init__()

    def receive_damage(self, eid, amount):
        bc = self.manager.get_entity_comp(eid, BaseEcsComponent.name())
        print('base receive damage', amount)
        bc.health -= amount
        if bc.health < 0:
            bc.health = 0
            self.manager.kill_entity(eid)

    def update(self, dt):
        # check for a ship in our radius
        phys_comp_list = self.manager.comps[phys.PhysicsEcsComponent.name()]
        coll_comp_list = self.manager.comps[collision.CollisionEcsComponent.name()]
        ship_comp_list = self.manager.comps[ship.ShipEcsComponent.name()]
        base_comp_list = self.manager.comps[BaseEcsComponent.name()]

        entities = self.manager.entities

        for idx, eid in enumerate(entities):
            basec = base_comp_list[idx]

            if basec:
                physc = phys_comp_list[idx]

                if basec.crew_load == 0:
                    continue

                for oidx, oeid in enumerate(entities):
                    if idx == oidx: continue
                    oshipc = ship_comp_list[oidx]

                    if oshipc:
                        ophysc = phys_comp_list[oidx]
                        if (physc.pos - ophysc.pos).length < basec.radius:
                            if basec.fuel_load:
                                fuel_required = oshipc.fuel_max - oshipc.fuel
                                if fuel_required:
                                    fuel_to_load = fuel_required
                                    self.manager.get_system(ship.ShipEcsSystem.name()).award_fuel(oeid, fuel_to_load)
                                    basec.fuel_load = False
                            if basec.crew_load:
                                self.manager.get_system(ship.ShipEcsSystem.name()).award_crew(oeid, basec.crew_load)
                                basec.crew_load = 0

                            if basec.repairs:
                                repair_required = oshipc.health_max - oshipc.health
                                if repair_required:
                                    repair_to_do = repair_required
                                    self.manager.get_system(ship.ShipEcsSystem.name()).award_health(oeid, repair_to_do)
                                    basec.repairs = False

    def on_entity_collision(self, e1id, e2id, impact_size, e1reflect, system_name, event):
        e1bc = self.manager.get_entity_comp(e1id, BaseEcsComponent.name())
        if e1bc:
            if self.manager.get_entity_comp(e2id, planet.PlanetEcsComponent.name()):
                self.manager.kill_entity(e1id)
            elif impact_size > e1bc.impact_resistance:
                damage = int(impact_size - e1bc.impact_resistance)
                if damage > 0:
                    self.receive_damage(e1id, damage)
            else:
                e1pc = self.manager.get_entity_comp(e1id, phys.PhysicsEcsComponent.name())
                e1pc.vel += e1reflect
