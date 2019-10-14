from .Component import *
from .Nav import Nav
from .Header import Header
from .Content import Content


class Row(Component):

    def __init__(self, content=[]):
        self.content = content
        self.layoutMode = "GRID_MODE"
        self._preprocess(self.content)

    def _preprocess(self, things):
        """
            In Ant Design, there are two Layouts: Grid(Row-Column) based or Layout(Header, Sider, Footer) based
            If we detect a Nav(), Header(), Content() we should not use Grid layout as that will break the relationship
            between these basic components
        """
        for t in things:
            if isinstance(t, Nav) or isinstance(t, Header) or isinstance(t, Content):
                self.layoutMode = "layoutMode"
                break

    def render(self):
        itemsToRender = []
        component = None
        if self.layoutMode == "layoutMode":
            for thing in self.content:
                itemsToRender.append(thing.render())
            component = (
                f"""<Layout>
                    {"".join(itemsToRender)}
                </Layout>
                """
            )
        else:
            avg = 24 // len(self.content)  # not robust, should do some check
            for thing in self.content:
                itemsToRender.append(
                    f"""<Col span={{{avg}}}>
                        {thing.render()}
                    </Col>
                    """
                )
            component = "".join(itemsToRender)

        return f"""
            <Row>
                {component}
            </Row>
        """
