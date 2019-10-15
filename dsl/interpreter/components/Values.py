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

COMPONENT = "Image"

class Image(Component):
    DEFAULT_ARGS = {
        "src": "process.env.PUBLIC_URL + '/logo.png'",
        "height": "100",
        "width": "100"
    }
    def __init__(self, args, rows):
        super().__init__(COMPONENT, self.DEFAULT_ARGS, args, rows)

    def render(self):
        return f"""<img alt="dsl example" src={self.getParamVal("src")} height="{self.getParamVal("height")}" width="{self.getParamVal("width")}" />"""
