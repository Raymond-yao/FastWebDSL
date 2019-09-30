from .Component import *
from .Row import Row
from .Header import *
from .Values import *
from .Nav import *


class Page(Component):
    def __init__(self, rows=[]):
        super().__init__()
        self.rows = []
        for r in rows:
            self.rows.append(Row(r))

    def add_row(self, row=[]):
        self.rows.append(Row(row))
        return self

    def render(self):
        things_to_render = []
        for stuff in self.rows:
            things_to_render.append(stuff.render())
        return f"""
            import React from "react";
            import ReactDOM from "react-dom";
            import {{Row, Col, Layout, Menu}} from "antd";
            import "antd/dist/antd.css";

            const {{Header, Sider, Content}} = Layout;

            ReactDOM.render(
                (<div id="Page">
                {"".join(things_to_render)}
                </div>),
                document.getElementById("root")
            );
        """
