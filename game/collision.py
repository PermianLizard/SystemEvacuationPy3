import math

from game import phys
from plib import ecs
from plib import vec2d


def get_circle_closest_point(pos, cpos, cradius):
    dv = math.sqrt(math.pow(cpos.x - pos.x, 2) + math.pow(cpos.y - pos.y, 2))
    cx = cpos.x + (cradius * (pos.x - cpos.x) / dv)
    cy = cpos.y + (cradius * (pos.y - cpos.y) / dv)

    return vec2d.vec2d(cx, cy)


class CollisionEcsComponent(ecs.EcsComponent):
    @classmethod
    def name(cls):
        return 'collision-component'

    def __init__(self, radius=0):
        super(CollisionEcsComponent, self).__init__()

        self.radius = radius


class CollisionEcsSystem(ecs.EcsSystem):
    @classmethod
    def name(cls):
        return 'collision-system'

    def __init__(self):
        super(CollisionEcsSystem, self).__init__()

    def update(self, dt):
        phys_comp_list = self.manager.comps[phys.PhysicsEcsComponent.name()]
        coll_comp_list = self.manager.comps[CollisionEcsComponent.name()]

        entities_to_remove = set()

        # we use this guy to keep track of the collision 'matrix'
        entity_collision_dict = {}

        entities = self.manager.entities
        for idx, eid in enumerate(entities):
            physc = phys_comp_list[idx]
            collc = coll_comp_list[idx]

            if physc == None or collc == None:
                continue

            for oidx, oeid in enumerate(entities):
                if eid == oeid: continue

                ophysc = phys_comp_list[oidx]
                ocollc = coll_comp_list[oidx]

                if ophysc == None or ocollc == None:
                    continue

                d = physc.pos.get_distance(ophysc.pos)
                coll_d = collc.radius + ocollc.radius

                if d <= coll_d:  # collision
                    e_coll_list = entity_collision_dict.setdefault(eid, [])
                    if oeid not in e_coll_list:
                        e_coll_list.append(oeid)
                        entity_collision_dict.setdefault(oeid, []).append(eid)

                        overlap = coll_d - d

                        # resolve the collision
                        dir = ophysc.pos - physc.pos

                        if physc.static:
                            dir.length = overlap
                            ophysc.pos = ophysc.pos + dir * 2
                        elif ophysc.static:
                            dir.length = overlap
                            physc.pos = ophysc.pos + dir * 2
                        else:
                            dir.length = overlap / 2
                            physc.pos = physc.pos - dir * 2
                            ophysc.pos = ophysc.pos + dir * 2

                        # calculate reflection here
                        ocontact_point = get_circle_closest_point(physc.pos, ophysc.pos, ocollc.radius)
                        normal = vec2d.vec2d(ocontact_point.x - ophysc.pos.x,
                                             ocontact_point.y - ophysc.pos.y).normalized()

                        incidence = (physc.vel) - (ophysc.vel)

                        mtotal = physc.mass + ophysc.mass
                        c1 = physc.mass / mtotal
                        c2 = ophysc.mass / mtotal

                        r = incidence - (2 * incidence.dot(normal)) * normal

                        impact_size = (ophysc.vel - physc.vel).length

                        angle = abs(r.get_angle_between(normal))

                        if angle > 1:
                            # print angle, angle * 0.3
                            mod = angle * 0.3

                            if r.length > mod:
                                r.length -= mod
                            else:
                                r.length = 0

                                # r.length /= (angle * 0.3)

                            # friction jobbie
                            # j = max(-(1 + 0.1) * physc.vel.dot(normal), 0.0)
                            # print j, impact_size
                            # r += normal * j

                            # contact.rigidBody->linearMomentum += j * contact.normal;

                        self.manager.entity_collision(eid, oeid, impact_size, r * c2, CollisionEcsSystem.name(),
                                                      'collision')
                        self.manager.entity_collision(oeid, eid, impact_size, ~r * c1, CollisionEcsSystem.name(),
                                                      'collision')

    def on_pre_remove_entity(self, eid, system_name, event):
        pass

        # print 'entity %s being removed by system "%s" because of "%s"' % (eid, system_name, event)

    def __str__(self):
        return 'CollisionEcsSystem'
