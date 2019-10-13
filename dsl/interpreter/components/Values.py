from .Component import *


class Text(Component):

    def render(self):
        return f"""<span>{self.value}</span>"""
