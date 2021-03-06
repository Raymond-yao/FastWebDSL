from .Component import *

COMPONENT = "Content"


class Content(Component):
    DEFAULT_ARGS = {
        "backgroud": "white"
    }

    def __init__(self, args, rows):
        super().__init__(COMPONENT, self.DEFAULT_ARGS, args, rows)

    def render(self):
        content = ""
        for row in self.rows:
            content += f'<div style={{{{ margin: "0 0 16px 0", padding: 24, background: "{self.getParamVal("backgroud")}" }}}}>'
            for item in row:
                content += item.render()
            content += "</div>"

        return f"""
            <Content style={{{{ overflow: 'initial' }}}}>
                {content}
            </Content>
        """
