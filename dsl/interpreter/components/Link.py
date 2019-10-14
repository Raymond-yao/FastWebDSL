from .Component import *

COMPONENT = "Link"


class Link(Component):
    DEFAULT_ARGS = {
        "to": "http://localhost:3000",
        "text": "link"
    }

    def __init__(self, args, rows):
        super().__init__(COMPONENT, self.DEFAULT_ARGS, args, rows)
        if len(rows) != 0:
            raise EvaluationError(
                COMPONENT, "link should not include sub-layout in it")
        href = self.getParamVal("to")
        self.href = "https://" + \
            href if "https://" not in href[0:8] else href

    def getHref(self):
        return f'"{self.href}"'

    def render(self):
        return f"""
            <Button
                type="link"
                class="{self.getParamVal("className")}"
                href="{self.getHref()}">
            {self.getParamVal("text")}
            </Button>
            """
