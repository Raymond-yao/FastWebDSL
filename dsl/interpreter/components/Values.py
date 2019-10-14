from .Component import *

COMPONENT = "Text"

class Text(Component):
    DEFAULT_ARGS = {
        "text": ""
    }
    def __init__(self, args, rows):
        super().__init__(COMPONENT, self.DEFAULT_ARGS, args, rows)

    def render(self):
        return f"""<span>{self.getParamVal("text")}</span>"""
