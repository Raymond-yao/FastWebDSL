from ..tokenizer.Token import *
"""
EBNF
    PROGRAM     ::= (ASSIGNMENT)* (LAYOUT)+
    ASSIGNMENT  ::= VAR “=” (VALUE | CONSTRUCTOR)
    VAR         ::= CHAR(CHAR | NUMBER | ” _”)*
    STRING      ::= \” CHAR(CHAR)* \”
    CHAR        ::= “a”-”z” | “A”-”Z”
    VALUE       ::= STRING | NUMBER | VAR
    CONSTRUCTOR ::= FUNCNAME | FUNCNAME “(” ASSIGNMENT (, ASSIGNMENT)*  “)”
    FUNCNAME    ::= “Nav” | “Header” | “Content” | “Link” | “Image” | “Video” | “Footer” | “Button”
    LAYOUT      ::= (VAR | “Page”) “{“ ROW(ROW)* “}”
    ROW         ::= "[" (VAR | CONSTRUCTOR) (“\s” (VAR | CONSTRUCTOR))* "]"
"""


class ASTNode:
    """
        Base class of ASTNode
    """

    def __init__(self, list_of_tokens):
        self.tokens = list_of_tokens

    def parse(self): pass

    def next(self):
        return self.tokens.pop(0)

    def has_next(self):
        return len(self.tokens) != 0

    def peek(self):
        return self.tokens[0]


class ProgramNode(ASTNode):

    def __init__(self, list_of_tokens):
        super().__init__(list_of_tokens)
        self.assignments = []
        self.layouts = []

    def parse(self):
        while self.has_next():
            tk = self.peek()
            if tk.is_a(Type.RESERVED) or tk.is_a(Type.VARIABLE):
                tk = self.tokens[1]
                if tk.is_a(Type.EQUAL):
                    new_assign_node = AssignmentNode(self.tokens)
                    self.assignments.append(new_assign_node)
                    new_assign_node.parse()
                elif tk.val == '{':
                    new_layout_node = LayoutNode(self.tokens)
                    self.layouts.append(new_layout_node)
                    new_layout_node.parse()
                else:
                    raise ParseError(
                        f"unexpected Token {repr(tk)}: expected a '=' to build an assignment or a '{{' to build a layout statement")
            else:
                raise ParseError(
                    f"unexpected Token {repr(tk)}: expected a variable or function keyword")


class AssignmentNode(ASTNode):

    STRING = "STRING"
    FUNC = "FUNC"
    NUM = "NUM"
    VAR = "VAR"  # we allow a1 = a2; a2 = a3 ... this brings challenges to determine referencing loop loool, e.g. a1 = a2; a2 = a1
    # (well not really hard, this is actually a graph loop detection from a fixed starting point, leetcode easy)

    TYPE_CONVERT_MAP = {
        Type.STRING: STRING,
        Type.NUMBER: NUM,
        Type.VARIABLE: VAR
    }

    def __init__(self, list_of_tokens):
        super().__init__(list_of_tokens)
        self.var_name = None
        self.assigned = None
        self.assignment_type = None

    def parse(self):
        self.var_name = self.next().value
        self.next()  # get rid of the '=' sign

        if not self.has_next():
            raise ParseError("reach the end of input unexpectedly")

        tk = self.peek()
        if tk.is_a(Type.RESERVED):
            self.assignment_type = self.FUNC
            self.assigned = ConstructorNode(self.tokens)
        elif tk.is_a(Type.STRING) or tk.is_a(Type.NUMBER) or tk.is_a(Type.VARIABLE):
            self.assignment_type = self.TYPE_CONVERT_MAP[tk.type]
            self.assigned = tk.value
            self.next()
        else:
            raise ParseError(
                f"unexpected Token {repr(tk)}: expected a string, number or constructor as an assigned value")


class ConstructorNode(ASTNode):

    def parse(self):
        return super().parse()  # TODO


class LayoutNode(ASTNode):

    def parse(self):
        return super().parse()  # TODO


class ParseError(Exception):
    def __init__(self, message):
        self.message = message
