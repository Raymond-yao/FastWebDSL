from .Component import *
from .Row import *

class Content(Component):

    def __init__(self, rows=[]):
        self.rows = []
        for r in rows:
            self.rows.append(Row(r))

    def render(self):
        things_to_render = []
        for row_comp in self.rows:
            things_to_render.append(row_comp.render())
        
        return f"""
            <Content>
                {"".join(things_to_render)}
            </Content>
        """