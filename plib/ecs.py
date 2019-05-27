from collections import OrderedDict

import pyglet


class EcsComponent(object):
    @classmethod
    def name(cls):
        return 'base-component'

    def __init__(self):
        self.name = self.name()

    def init(self):
        pass

    def cleanup(self):
        pass

    def __str__(self):
        return 'EcsComponent'


class EcsSystem(object):
    @classmethod
    def name(cls):
        return 'base-system'

    def __init__(self):
        self.name = self.name()
        self.manager = None

    def init(self):
        pass

    def cleanup(self):
        pass

    def draw(self):
        pass

    def update(self, dt):
        pass

    def on_create_entity(self, eid, system_name, event):
        pass

    def on_pre_remove_entity(self, eid, system_name, event):
        pass

    def on_post_remove_entity(self, eid, system_name, event):
        pass

    def __str__(self):
        return 'EcsSystem'


class EcsRenderer(object):
    @classmethod
    def name(cls):
        return 'base-renderer'

    def __init__(self):
        self.name = self.name()
        self.manager = None

    def init(self):
        pass

    def cleanup(self):
        pass

    def draw(self):
        pass

    def on_create_entity(self, eid, system_name, event):
        pass

    def on_pre_remove_entity(self, eid, system_name, event):
        pass

    def on_post_remove_entity(self, eid, system_name, event):
        pass

    def __str__(self):
        return 'EcsRenderer'


class EcsInputHandler(object):
    @classmethod
    def name(cls):
        return 'base-input-handler'

    def __init__(self):
        self.name = self.name()
        self.manager = None

    def init(self):
        pass

    def cleanup(self):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_enter(self, x, y):
        pass

    def on_mouse_leave(self, x, y):
        pass

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        pass

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass

    def on_create_entity(self, eid, system_name, event):
        pass

    def on_pre_remove_entity(self, eid, system_name, event):
        pass

    def on_post_remove_entity(self, eid, system_name, event):
        pass


class EcsManager(pyglet.event.EventDispatcher):
    def __init__(self):
        self.entity_count = 0
        self.systems = OrderedDict()
        self.renderers = OrderedDict()
        self.input_handlers = OrderedDict()
        self.entities = []
        self.comps = {}
        self.keys = None

    def reg_comp_type(self, name):
        if name not in self.comps:
            self.comps[name] = []

    def add_system(self, system):
        self.systems[system.name] = system
        system.manager = self

    def get_system(self, name):
        return self.systems[name]

    def add_renderer(self, renderer):
        self.renderers[renderer.name] = renderer
        renderer.manager = self

    def get_renderer(self, name):
        return self.renderers[name]

    def add_input_handler(self, input_handler):
        self.input_handlers[input_handler.name] = input_handler
        input_handler.manager = self

    def get_input_handler(self, name):
        return self.input_handlers[name]

    def setup_handlers(self):
        for system in self.systems.values():
            self.push_handlers(system)

        for renderer in self.renderers.values():
            self.push_handlers(renderer)

            # for input_handler in self.input_handlers.values():
        #	self.push_handlers(input_handler)

    def init(self):
        for system in self.systems.values():
            system.init()

        for renderer in self.renderers.values():
            renderer.init()

        for input_handler in self.input_handlers.values():
            input_handler.init()

    def cleanup(self):
        try:
            self.pop_handlers()
        except AssertionError as e:
            print('assertion error on ECS Manager pop_handlers()')

        for system in self.systems.values():
            system.cleanup()

        for renderer in self.renderers.values():
            renderer.cleanup()

        for input_handler in self.input_handlers.values():
            input_handler.cleanup()

    def create_entity(self, comps=[], system_name='', event=''):
        self.entity_count += 1

        eid = self.entity_count

        self.entities.append(self.entity_count)
        for name, lst in self.comps.items():
            supplied = False
            for comp in comps:
                if comp.name == name:
                    # lst.append(copy.deepcopy(comp))
                    lst.append(comp)
                    supplied = True
            if not supplied:
                lst.append(None)

        self.dispatch_event('on_create_entity', eid, system_name, event)

        return eid

    def remove_entity(self, eid, system_name='', event=''):
        idx = self.entities.index(eid)

        self.dispatch_event('on_pre_remove_entity', eid, system_name, event)

        del self.entities[idx]
        for name, lst in self.comps.items():
            del lst[idx]

        self.dispatch_event('on_post_remove_entity', eid, system_name, event)

    def get_entity_comp(self, eid, name):
        try:
            idx = self.entities.index(eid)
            return self.comps[name][idx]
        except:
            return None

    def get_entity_comps(self, eid):
        idx = self.entities.index(eid)
        comps = []
        for comp_name, comp_list in self.comps.items():
            comp = comp_list[idx]
            if comp: comps.append(comp)
        return comps

    def draw(self):
        for renderer in self.renderers.values():
            renderer.draw()

    def update(self, dt):
        for system in self.systems.values():
            system.update(dt)

    def on_mouse_motion(self, x, y, dx, dy):
        for input_handler in self.input_handlers.values():
            input_handler.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        for input_handler in self.input_handlers.values():
            input_handler.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        for input_handler in self.input_handlers.values():
            input_handler.on_mouse_release(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        for input_handler in self.input_handlers.values():
            input_handler.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_enter(self, x, y):
        for input_handler in self.input_handlers.values():
            input_handler.on_mouse_enter(x, y)

    def on_mouse_leave(self, x, y):
        for input_handler in self.input_handlers.values():
            input_handler.on_mouse_leave(x, y)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        for input_handler in self.input_handlers.values():
            input_handler.on_mouse_scroll(x, y, scroll_x, scroll_y)

    def on_key_press(self, symbol, modifiers):
        for input_handler in self.input_handlers.values():
            input_handler.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        for input_handler in self.input_handlers.values():
            input_handler.on_key_release(symbol, modifiers)


EcsManager.register_event_type('on_create_entity')
EcsManager.register_event_type('on_pre_remove_entity')
EcsManager.register_event_type('on_post_remove_entity')
