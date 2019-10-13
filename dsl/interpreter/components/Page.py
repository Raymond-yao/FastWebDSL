from .Component import *
from .Row import Row
from .Header import *
from .Values import *
from .Nav import *


class Page(Component):

    def add_row(self, row=[]):
        self.rows.append(Row(row))
        return self

    def render(self):
        things_to_render = []
        for stuff in self.rows:
            to_render = []
            for e in stuff:
                to_render.append(e.render())
            things_to_render.append("".join(to_render))
        return f"""
            import React from "react";
            import ReactDOM from "react-dom";
            import {{ Row, Col, Layout, Menu }} from "antd";
            import "antd/dist/antd.css";

            const {{ Header, Sider, Content }} = Layout;

            ReactDOM.render(
                (<div id="Page">
                {"".join(things_to_render)}
                </div>),
                document.getElementById("root")
            );
        """
