import os
import pyglet

from game import start

FONT_MONO = None

def init():
	PATH = os.path.join(start.DATA_PATH, 'fonts')

	pyglet.font.add_file(os.path.join(PATH, 'Mono.ttf'))
	
	global FONT_MONO
	FONT_MONO = pyglet.font.load('mono 07_56')