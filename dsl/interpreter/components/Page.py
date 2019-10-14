from .Component import *
from .Row import Row
from .Header import *
from .Values import *
from .Nav import *

COMPONENT = "Page"


class Page(Component):
    def __init__(self, args, rows):
        super().__init__(COMPONENT, {}, args, rows)
        self.rows = []
        for row in rows:
            self.rows.append(Row(row))

    def render(self):
        rows = ""
        for row in self.rows:
            rows += row.render() + "\n"
        return f"""
            <Layout>
                {rows}
            </Layout>
        """
