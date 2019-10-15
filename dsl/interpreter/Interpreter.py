from .components.ComponentFactory import *
from ..parser.ASTNode import *


class Interpreter:

    def __init__(self, astRoot, comp_factory):
        self.factory = comp_factory
        self.ast = astRoot
        self.env = ASTNode.dereference_dict

    def handle_layout(self, astNode):
        component_builder = self.factory.get(astNode.layoutType)
        params = {}
        if astNode.layoutType != "Page":
            params = self.env[astNode.layoutName]["constructor"].attr

        rows_to_add = []
        for rowNode in astNode.rows:
            rows_to_add.append(self.handle_row(rowNode))

        return component_builder(params, rows_to_add)

    def handle_row(self, rowNode):
        elems = []
        for e in rowNode.elements:
            elems.append(self.handle_node_in_row(e))

        return elems

    def handle_node_in_row(self, node):
        if isinstance(node, str):
            return self.factory.get("Text")({"text": node}, [])
        elif isinstance(node, VarNode):
            if node.varName in self.env:
                return self.handle_node_in_row(self.env[node.varName])
            else:
                raise RuntimeError(f"free identifier {node.varName}")
        elif isinstance(node, dict):
            if node["layout"] != None:
                return self.handle_layout(node["layout"])
            else:
                return self.handle_node_in_row(node["constructor"])
        elif isinstance(node, ConstructorNode):
            return self.factory.get(node.constructor_name)(node.attr, [])
        else:
            raise RuntimeError(f"Unrecognized Row element {node}")

    def interp(self):
        layout_root = None
        for l in self.ast.layouts:
            if l.layoutType == "Page":
                layout_root = l

        if layout_root == None:
            raise RuntimeError("missing Page Layout")

        return self.handle_layout(layout_root).render()


class RuntimeError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.message = msg


def evaluate(ast):
    return f"""
        export default class App extends React.Component {{
        render() {{
            return (
            <div>
                {Interpreter(ast, RealComponentFactory()).interp()}
            </div>
            )
        }}
        }}
    """
