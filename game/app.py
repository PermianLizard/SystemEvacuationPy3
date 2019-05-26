from plib import director
from game import font
from game import img
from game import anim
from game import menu
from game import instruct
from game import game as g
from game import map
from game import end

def init():
	font.init()
	img.init()
	anim.init()
	menu.init()
	instruct.init()
	g.init()
	map.init()
	end.init()
	director.director.push(menu.menu_scene)

def cleanup():
	pass