import os
import logging
from optparse import OptionParser
import pyglet
from pyglet import gl
import plib.director
import plib.scene

from game import app

DATA_PATH = os.path.join(os.path.abspath(pyglet.resource.get_script_home()), 'data')
pyglet.resource.path.append(DATA_PATH)
pyglet.resource.reindex()

from game.const import APP_NAME, PROJECT_DESC, PROJECT_URL, VERSION, WIDTH, HEIGHT, AUDIO_DRIVERS

def on_cleanup():
	app.cleanup()

def run():
	pyglet.options['audio'] = AUDIO_DRIVERS
	pyglet.options['debug_gl'] = False

	parser = OptionParser(description="%s: %s" % (APP_NAME, PROJECT_DESC),
		epilog='Project website: %s' % PROJECT_URL,
		version='%s %s' % (APP_NAME, VERSION),
	)
	parser.add_option("-f", "--fullscreen",
		dest="fullscreen",
		default=False,
		action="store_true",
	)
	parser.add_option("-d", "--debug",
		dest="debug",
		default=False,
		action="store_true",
	)
	options, args = parser.parse_args()

	if options.debug:
		logging.basicConfig(level=logging.DEBUG)
		logging.debug("Debug enabled")
		logging.debug("Options: %s" % options)

	gl.glEnable(gl.GL_BLEND)                                                            
	gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
	gl.glEnable(gl.GL_LINE_SMOOTH);                                                     
	gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_DONT_CARE) 

	plib.director.director.init(width=WIDTH, 
		height=HEIGHT, 
		fullscreen=options.fullscreen, 
		caption=APP_NAME,
		debug=options.debug)

	plib.director.director.on_cleanup = on_cleanup

	app.init()

	plib.director.director.run()