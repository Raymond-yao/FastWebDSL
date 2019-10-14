from .Component import *

COMPONENT = "Footer"


class Footer(Component):
    DEFAULT_ARGS = {
        "align": "center",
        "text": "Powered by Fast Web DSL"
    }

    def __init__(self, args, rows):
        super().__init__(COMPONENT, self.DEFAULT_ARGS, args, rows)
        if len(rows) != 0:
            raise EvaluationError(
                COMPONENT, "footer should not include sub-layout in it")

    def render(self):
        return f"""
            <Footer style={{{{ textAlign: '{self.getParamVal("align")}' }}}}>
                {self.getParamVal("text")}
            </Footer>
            """
