import logging

import pyglet
from pyglet import gl


class Director(pyglet.event.EventDispatcher):
    def __init__(self):
        self._initialized = False
        self._width = None
        self._height = None
        self._window = None
        self._keys = None
        self._fullscreen = False
        self._debug = False
        self._fps = None
        self._fps_clock = None
        self._ticks = None
        self._scene_stack = []

        self._viewport_width = None
        self._viewport_height = None
        self._viewport_x_offs = None
        self._viewport_y_offs = None

    @property
    def initialized(self):
        return self._initialized

    @property
    def scene(self):
        if len(self._scene_stack):
            return self._scene_stack[-1]
        return None

    @property
    def scene_count(self):
        return len(self._scene_stack)

    @property
    def window(self):
        return self._window

    @property
    def viewport(self):
        return (self._viewport_x_offs, self._viewport_y_offs, self._viewport_width, self._viewport_height)

    @property
    def keys(self):
        return self._keys

    @property
    def fps(self):
        return self._fps

    def init(self, width=800, height=600, fullscreen=False, caption="Title", fps=60.0, debug=False):
        if self._initialized:
            self.cleanup()

        self._fullscreen = fullscreen
        self._debug = debug

        self._width = width
        self._height = height

        self._window = pyglet.window.Window(width, height, caption=caption, resizable=False, vsync=False)
        if self._fullscreen:
            self._window.set_fullscreen(True)
        else:
            self._window.set_minimum_size(width, height)

        if self._debug:
            self._fps_clock = pyglet.window.FPSDisplay(self._window)

        self._fps = float(fps)
        self._ticks = 0

        self._window.on_draw = self._draw
        self._window.on_resize = self._resize
        self._window.on_mouse_motion = self._on_mouse_motion
        self._window.on_mouse_press = self._on_mouse_press
        self._window.on_mouse_release = self._on_mouse_release
        self._window.on_mouse_drag = self._on_mouse_drag
        self._window.on_mouse_enter = self._on_mouse_enter
        self._window.on_mouse_leave = self._on_mouse_leave
        self._window.on_mouse_scroll = self._on_mouse_scroll
        self._window.on_key_press = self._on_key_press
        self._window.on_key_release = self._on_key_release

        self._keys = pyglet.window.key.KeyStateHandler()
        self._window.push_handlers(self._keys)

        self._initialized = True

        logging.debug("director initialized")

    def cleanup(self):
        self._window.remove_handlers()
        self._fullscreen = False
        self._initialized = False

        self.dispatch_event('on_cleanup')

    def run(self):
        if not self._initialized:
            self.init()
        pyglet.clock.schedule_interval(self._update, 1 / self._fps)
        pyglet.app.run()

    def stop(self):
        pyglet.clock.unschedule(self._update)
        pyglet.app.exit()

        self.dispatch_event('on_stop')

    def push(self, scene):
        if self.scene:
            self.scene.pause()
        self._scene_stack.append(scene)
        scene.enter()

    def pop(self):
        scene = self._scene_stack.pop()
        scene.exit()
        if self.scene:
            self.scene.unpause()
        else:
            self.stop()
            self.cleanup()

    def replace(self, scene):
        self._scene_stack.pop().exit()
        self._scene_stack.append(scene)
        scene.enter()

    def _update(self, dt):
        if self.scene_count:
            self.scene.update(dt)
            self._ticks += 1

    def _draw(self):
        self._window.clear()

        if self.scene_count:
            self.scene.draw()

        if self._debug:
            self._fps_clock.draw()

    def _resize(self, width, height):
        aspect = float(self._width) / self._height

        self._viewport_width = int(min(width, height * aspect))
        self._viewport_height = int(min(height, width / aspect))
        self._viewport_x_offs = (width - self._viewport_width) // 2
        self._viewport_y_offs = (height - self._viewport_height) // 2

        x = (width - self._width) / 2
        gl.glViewport(self._viewport_x_offs,
                      self._viewport_y_offs,
                      self._viewport_width,
                      self._viewport_height,
                      )
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, self._viewport_width, 0, self._viewport_height, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        logging.debug("Viewport: %s, %s, %s, %s" % (self._viewport_x_offs,
                                                    self._viewport_y_offs,
                                                    self._viewport_width,
                                                    self._viewport_height,
                                                    ))

    def _on_mouse_motion(self, x, y, dx, dy):
        if self.scene_count:
            self.scene.on_mouse_motion(x, y, dx, dy)

    def _on_mouse_press(self, x, y, button, modifiers):
        if self.scene_count:
            self.scene.on_mouse_press(x, y, button, modifiers)

    def _on_mouse_release(self, x, y, button, modifiers):
        if self.scene_count:
            self.scene.on_mouse_release(x, y, button, modifiers)

    def _on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.scene_count:
            self.scene.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def _on_mouse_enter(self, x, y):
        if self.scene_count:
            self.scene.on_mouse_enter(x, y)

    def _on_mouse_leave(self, x, y):
        if self.scene_count:
            self.scene.on_mouse_leave(x, y)

    def _on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.scene_count:
            self.scene.on_mouse_scroll(x, y, scroll_x, scroll_y)

    def _on_key_press(self, symbol, modifiers):
        if self.scene_count:
            self.scene.on_key_press(symbol, modifiers)

    def _on_key_release(self, symbol, modifiers):
        if self.scene_count:
            self.scene.on_key_release(symbol, modifiers)


Director.register_event_type('on_stop')
Director.register_event_type('on_cleanup')

director = Director()
