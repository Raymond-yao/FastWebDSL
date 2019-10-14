from ..components.ComponentFactory import *
from ..components.Component import Component


class Dummy(Component):

    def __init__(self, name, params, rows):
        self.params = params
        self.rows = rows
        self.name = name

    def render(self):
        to_render = []
        for r in self.rows:
            sth = []
            for e in r:
                sth.append(e.render())
            to_render.append(sth)

        return {
            "name": self.name,
            "params": self.params,
            "rows": to_render
        }


class TestFactory(RealComponentFactory):

    def __init__(self):
        super().__init__()

    def get(self, component_name):
        return lambda params, rows: Dummy(component_name, params, rows)
