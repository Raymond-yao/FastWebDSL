from Component import *

class Text(Component):

    def __init__(self, text):
        self.value = text

    def render(self):
        return f"""<span>{self.value}</span>"""