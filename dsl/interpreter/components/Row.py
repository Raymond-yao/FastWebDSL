from .Component import *
from .Nav import Nav
from .Header import Header


class Row(Component):

    def __init__(self, content=[]):
        super().__init__()
        self.content = content
        self.layout_mode = "ROW_COLUMN_MODE"
        self.preprocess(self.content)

    def preprocess(self, things):
        """
            In Ant Design, there are two Layouts: Grid(Row-Column) based or Layout(Header, Sider, Footer) based
            If we detect a Nav(), Header(), Content() we should not use Grid layout as that will break the relationship
            between these basic components
        """
        for t in things:
            if isinstance(t, Nav) or isinstance(t, Header):  # TODO: add Content()
                self.layout_mode = "CLASSIC_MODE"
                break

    def render(self):
        things_to_render = []
        component = None
        if self.layout_mode == "CLASSIC_MODE":
            for thing in self.content:
                things_to_render.append(thing.render())
            component = (
                f"""<Layout>
                    {"".join(things_to_render)}
                </Layout>
                """
            )
        else:
            avg = 24 // len(self.content)  # not robust, should do some check
            for thing in self.content:
                things_to_render.append(
                    f"""<Col span={{{avg}}}>
                        {thing.render()}
                    </Col>
                    """
                )
            component = "".join(things_to_render)

        return f"""
            <Row>
                {component}
            </Row>
        """
