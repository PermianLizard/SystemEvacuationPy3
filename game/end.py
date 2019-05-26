import pyglet
from pyglet import gl
from plib.director import director
import plib.scene

from game import font
from game import menu

victory_scene = None

def init():
	global victory_scene
	victory_scene = VictoryScene()


class VictoryScene(plib.scene.Scene):
	def __init__(self):
		super(VictoryScene, self).__init__()

		self.label = pyglet.text.Label('Victory',
			font_name=font.FONT_MONO.name,
			font_size=36,
			x=500//2, y=300//2,
			anchor_x='center', anchor_y='center')

	def draw(self):
		self.label.draw()

		gl.glBegin(pyglet.gl.GL_TRIANGLES)
		gl.glVertex2f(0, 0)
		gl.glVertex2f(100, 0)
		gl.glVertex2f(100, 200)
		gl.glEnd()

		#gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
		#gl.glLoadIdentity()
		#vp = director.viewport
		#gl.glBegin(pyglet.gl.GL_QUADS)
		#gl.glVertex2f(0 , 0)
		#gl.glVertex2f(vp[2], 0)
		#gl.glVertex2f(vp[2], vp[3])
		#gl.glVertex2f(0, vp[3])
		#gl.glEnd()

	def on_key_press(self, symbol, modifiers):
		super(VictoryScene, self).on_key_press(symbol, modifiers)

		#if symbol == pyglet.window.key.ENTER:
		#	director.push(game.game_scene)
		#if symbol == pyglet.window.key.Q:
		#	director.pop()

