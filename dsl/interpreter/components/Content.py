from .Component import *
from .Row import *


class Content(Component):

    def render(self):
        things_to_render = []
        for row_comp in self.rows:
            things_to_render.append(row_comp.render())

        return f"""
            <Content>
                {"".join(things_to_render)}
            </Content>
        """
