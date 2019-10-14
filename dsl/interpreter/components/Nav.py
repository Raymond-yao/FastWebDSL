from .Component import *
from .Values import *
from .Link import *

COMPONENT = "Nav"


class Nav(Component):
    DEFAULT_ARGS = {
        "size": "medium",
        "theme": "dark",
    }

    def __init__(self, args, rows):
        super().__init__(COMPONENT, self.DEFAULT_ARGS,
                         args, rows, NavFactory.ARG_TO_ATTR_MAP)

    def render(self):
        navFactory = NavFactory(self.args, self.rows)
        return f"""
            <Sider {navFactory.getSiderAttr()}>
                <Menu {navFactory.getMenuAttr()}>
                    {navFactory.getItems()}
                </Menu>
            </Sider>"""


class NavFactory:
    ARG_TO_ATTR_MAP = {
        "size": {
            "small": 150,
            "medium": 230,
            "large": 330
        }
    }

    def __init__(self, args, rows):
        self.args = args
        self.rows = rows
        self.__createAttrs()

    def getSiderAttr(self):
        return self.siderAttr

    def getMenuAttr(self):
        return self.menuAttr

    def getItems(self):
        items = ""
        for i, row in enumerate(self.rows):
            if len(row) != 1:
                raise EvaluationError(
                    COMPONENT, "each row in Nav should have exactly one item")
            component_in_row = row[0]
            if isinstance(component_in_row, Text):
                items += f'<Menu.Item key="{i}">{component_in_row.getParamVal("text")}</Menu.Item>\n'
            elif isinstance(component_in_row, Link):
                items += f'<Menu.Item key="{i}" onClick={{() => window.location.href = {component_in_row.getHref()} }}>{component_in_row.getParamVal("text")}</Menu.Item>\n'
            else:
                raise EvaluationError(
                    COMPONENT, "only Text and Link components are allowed")
        return items

    def __createAttrs(self):
        self.siderAttr = f"""
            width={{{self.ARG_TO_ATTR_MAP["size"][self.args["size"]]}}} style={{{{ minHeight: '100vh' }}}}
        """
        self.menuAttr = ""
