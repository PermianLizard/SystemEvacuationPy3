import pyglet
from plib import ecs
from game import ship


class PlayerIdentityEcsComponent(ecs.EcsComponent):

	@classmethod
	def name(cls):
		return 'player-identity-component'

	def __init__(self):
		super(PlayerIdentityEcsComponent, self).__init__()


class PlayerEscInputHandler(ecs.EcsInputHandler):

	@classmethod
	def name(cls):
		return 'player-input-handler'

	def __init__(self):
		super(PlayerEscInputHandler, self).__init__()
		self.player_entity_id = None

	def init(self):
		self.player_entity_id = None

		player_comp_list = self.manager.comps[PlayerIdentityEcsComponent.name()]
		for idx, eid in enumerate(self.manager.entities):
			if player_comp_list[idx]:
				self.player_entity_id = eid

	def on_key_press(self, symbol, modifiers):
		if self.player_entity_id:
			# TODO: player action here
			if symbol == pyglet.window.key.LEFT:
				pass
			elif symbol == pyglet.window.key.RIGHT:
				pass


class PlayerEscSystem(ecs.EcsSystem):

	@classmethod
	def name(cls):
		return 'player-system'

	def __init__(self):
		super(PlayerEscSystem, self).__init__()
		self.player_entity_id = None

	def init(self):
		self.player_entity_id = None

		player_comp_list = self.manager.comps[PlayerIdentityEcsComponent.name()]
		for idx, eid in enumerate(self.manager.entities):
			if player_comp_list[idx]:
				self.player_entity_id = eid

		self.time_limit = 17000

	def on_crew_rescued(self, eid, amount):
		if eid == self.player_entity_id:
			sc = self.manager.get_entity_comp(eid, ship.ShipEcsComponent.name())
			if sc.passengers == self.manager.crew_to_rescue:
				self.manager.declare_victory(PlayerEscSystem.name(), 'all crew rescued')

	def on_pre_remove_entity(self, eid, system_name, event):
		if eid == self.player_entity_id:
			self.manager.declare_defeat(PlayerEscSystem.name(), 'your ship has been destroyed')

	def update(self, dt):
		if not self.player_entity_id or self.player_entity_id not in self.manager.entities:
			return

		if self.manager.keys[pyglet.window.key.LEFT] or self.manager.keys[pyglet.window.key.A]:
			self.manager.get_system(ship.ShipEcsSystem.name()).turn_left(self.player_entity_id)
		elif self.manager.keys[pyglet.window.key.RIGHT] or self.manager.keys[pyglet.window.key.D]:
			self.manager.get_system(ship.ShipEcsSystem.name()).turn_right(self.player_entity_id)
		elif self.manager.keys[pyglet.window.key.UP] or self.manager.keys[pyglet.window.key.W]:
			self.manager.get_system(ship.ShipEcsSystem.name()).thrust_forward(self.player_entity_id)

		if self.time_limit:
			self.time_limit -= 1
			if self.time_limit == 0:
				self.manager.declare_defeat(PlayerEscSystem.name(), 'your ran out of time')