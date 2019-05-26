import pyglet
from pyglet import gl
import random


class Starfield(object):
	def __init__(self, area, size):
		self.area = area
		self.size = size

		self._generate()

	def draw(self, xoffset, yoffset):
		self._update(xoffset, yoffset)
		self._vertex_list.draw(gl.GL_POINTS)

	def _update(self, xoffset, yoffset):
		area = self.area
		vertices = self.vertices
		depths = self.depths

		xaxis = True
		depth = 0
		for idx, v in enumerate(vertices):
			if xaxis:
				depth = self.depths[idx // 2]
				value = ((vertices[idx] - xoffset * depth) % area[2]) + area[0]
			else:
				value = ((vertices[idx] - yoffset * depth) % area[3]) + area[1]
			self._vertex_list.vertices[idx] = value
			xaxis = not xaxis

	def _generate(self):
		area = self.area
		size = self.size

		vertices = []
		depths = []
		colors = []

		for i in range(size):
			x = random.uniform(area[0], area[0] + area[2])
			y = random.uniform(area[1], area[1] + area[3])
			d = random.uniform(0.5, 1.0)

			vertices.append(x)
			vertices.append(y)

			depths.append(d)

			r = random.uniform(0.9, 1)
			g = random.uniform(0.9, 1)
			b = random.uniform(0.9, 1)

			colors.append(r)
			colors.append(g)
			colors.append(b)

		self._vertex_list = pyglet.graphics.vertex_list(size,
			('v2f/stream', vertices),
			('c3f/static', colors),
		)

		self.vertices = vertices
		self.depths = depths