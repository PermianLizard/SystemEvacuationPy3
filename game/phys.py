import math

from plib import vec2d
from plib import ecs

GRAV_CONSTANT = 2
SPEED_LIMIT = 180


class PhysicsEcsComponent(ecs.EcsComponent):

	@classmethod
	def name(cls):
		return 'physics-component'

	def __init__(self, x, y, mass, static=False, vx=0.0, vy=0.0):
		super(PhysicsEcsComponent, self).__init__()
		self.pos = vec2d.vec2d(x, y)
		self.vel = vec2d.vec2d(vx, vy)
		self.acc = vec2d.vec2d(0, 0)
		self.mass = float(mass)
		self.static = static

	def apply_force(self, x, y):
		force = vec2d.vec2d(x / self.mass, y / self.mass)
		self.vel = self.vel + force

	def update(self, dt):
		if not self.static:
			self.vel += self.acc * dt
			if self.vel.length > SPEED_LIMIT:
				self.vel.length = SPEED_LIMIT
			self.pos += self.vel * dt

	def __str__(self):
		return 'PhysicsEcsComponent'


class GravityEcsComponent(ecs.EcsComponent):

	@classmethod
	def name(cls):
		return 'gravity-component'

	def __init__(self, gravity_radius=0):
		super(GravityEcsComponent, self).__init__()
		self.gravity_radius = gravity_radius

	def __str__(self):
		return 'GravityEcsComponent'


class PhysicsEcsSystem(ecs.EcsSystem):

	@classmethod
	def name(cls):
		return 'physics-system'

	def __init__(self):
		super(PhysicsEcsSystem, self).__init__()

	def set_orbit(self, e1, e2, distance, angle_in_degrees, clockwise=True):
		pc1 = self.manager.get_entity_comp(e1, PhysicsEcsComponent.name())
		pc2 = self.manager.get_entity_comp(e2, PhysicsEcsComponent.name())

		if pc1 == None or pc2 == None:
			return

		# TODO what if we want to orbit from where we are? ie no angle specified
		rad = math.radians(angle_in_degrees)
		x = pc2.pos.x + distance * math.cos(rad)
		y = pc2.pos.y + distance * math.sin(rad)
		pc1.pos.x = x
		pc1.pos.y = y

		gv = (pc1.pos - pc2.pos).normalized()
		ov = vec2d.vec2d(gv.y, gv.x)

		if clockwise:
			ov.y *= -1
		else:
			ov.x *= -1

		mag = math.sqrt((GRAV_CONSTANT * pc2.mass) / distance)
		ov *= mag
		pc1.vel = ov
		pc1.acc = vec2d.vec2d(0, 0) # make acceleration zero

	def update(self, dt):
		phys_comp_list = self.manager.comps[PhysicsEcsComponent.name()]
		grav_comp_list = self.manager.comps[GravityEcsComponent.name()]

		# gravity
		for idx, gc in enumerate(grav_comp_list):
			if not gc: continue
			pc = phys_comp_list[idx]
			if not pc:
				continue

			for o_pc in phys_comp_list:
				if not o_pc:
					continue

				if pc == o_pc: 
					continue
				if o_pc.static:
					continue

				d = pc.pos.get_distance(o_pc.pos)

				# gravity cutoff point
				if gc.gravity_radius < d:
					continue

				f = GRAV_CONSTANT * pc.mass * o_pc.mass / d ** 2
				fv = (pc.pos - o_pc.pos).normalized() * f * dt
				o_pc.apply_force(fv.x, fv.y)

		for pc in phys_comp_list:
			if not pc:
				continue
			pc.update(dt)

	def __str__(self):
		return 'PhysicsEcsSystem'