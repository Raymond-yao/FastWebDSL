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

    names = []
    constructor_def = {
        "Nav": [
            {"name": "size", "expected_type": "number", "default": 100},
            {"name": "colour", "expected_type": "string", "default": "black"},
            {}
        ],
        "Header": []
    }

    default_nav_attr = {'size': 'small', 'align': 'left', 'background': '#D4F2FC'}
    default_header_attr = {'title': 'Header', 'background': 'black'}
    default_content_attr = {}
    default_link_attr = {}
    default_image_attr = {}
    default_video_attr = {}
    default_footer_attr = {}
    default_button_attr = {}
    default_page_attr = {}

    def __init__(self, list_of_tokens):
        self.tokens = list_of_tokens

    def parse(self):
        self.next()

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

    # TODO: validate whether page root exist

    def parse(self):
        while self.has_next():
            tk = self.peek()
            if tk.is_a(Type.RESERVED) or tk.is_a(Type.VARIABLE):
                if len(self.tokens) < 3:
                    raise ParseError(
                        "unexpected line end: must have an assignment statement or a layout statement")
                tk = self.tokens[1]
                if tk.is_a(Type.EQUAL):
                    new_assign_node = AssignmentNode(self.tokens)
                    self.assignments.append(new_assign_node)
                    new_assign_node.parse()
                elif tk.value == '{':
                    new_layout_node = LayoutNode(self.tokens)
                    self.layouts.append(new_layout_node)
                    new_layout_node.parse()
                else:
                    raise ParseError(
                        f"unexpected Token {repr(tk)}: expected a '=' to build an assignment or a '{{' to build a layout statement")
            else:
                raise ParseError(
                    f"unexpected Token {repr(tk)}: expected a variable or function keyword")

    def name_check(self):
        for a in self.assignments:
            a.name_check()
        for l in self.layouts:
            l.name_check()

    def type_check(self):
        for a in self.assignments:
            a.type_check()
        for l in self.layouts:
            l.type_check()


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
        self.tk = None

    def parse(self):
        if len(self.tokens) < 3:
            raise ParseError(
                "reach the end of input unexpectedly, not a valid assignment statement")
        self.var_name = self.next().value
        if self.peek() != Eq():
            raise ParseError("unexpected char %s, expecting %s " %
                             (self.next().value, "="))
        self.next()  # get rid of the '=' sign

        if not self.has_next():
            raise ParseError(
                "reach the end of input unexpectedly, not a valid assignment statement")

        self.tk = self.peek()
        if self.tk.is_a(Type.RESERVED):
            self.assignment_type = self.FUNC
            self.assigned = ConstructorNode(self.tokens)
            self.assigned.parse()
        elif self.tk.is_a(Type.STRING) or self.tk.is_a(Type.NUMBER) or self.tk.is_a(Type.VARIABLE):
            self.assignment_type = self.TYPE_CONVERT_MAP[self.tk.type]
            self.assigned = self.tk.value
            self.next()
        else:
            raise ParseError(
                f"unexpected Token {repr(self.tk)}: expected a string, number or constructor as an assigned value")

    def name_check(self):
        ASTNode.names.append(self.var_name)
        if self.assignment_type == self.TYPE_CONVERT_MAP[Type.VARIABLE] and self.assigned not in self.names:
            raise NameCheckError(self.assigned)
        if self.assignment_type == self.FUNC:
            self.assigned.name_check()

    def type_check(self):
        if self.assignment_type == self.FUNC:
            self.assigned.type_check(self.tk)


class ConstructorNode(ASTNode):
    def __init__(self, list_of_tokens):
        super().__init__(list_of_tokens)
        self.params = []
        self.attr = {}

    def parse(self):
        if len(self.tokens) < 3 or Bracket("(") not in self.tokens or Bracket(")") not in self.tokens:
            raise ParseError(
                "unexpected line end: constructor declaration must be in this form: Constructor()")
        if self.tokens.count(Bracket("(")) != self.tokens.count(Bracket(")")):
            raise ParseError(
                "unexpected line end: number of opening and closing bracket does not match")
        # I'll use a copy of self.token to create assignment node
        # then use "move" to pop that much of tokens from self.token
        move = 3
        constructorParam = self.tokens[self.tokens.index(
            Bracket("(")) + 1: self.tokens.index(Bracket(")"))]
        # else it's default constructor
        if len(constructorParam) != 0:
            move += len(constructorParam)
            if Bracket("(") in constructorParam or Bracket(")") in constructorParam:
                raise ParseError(
                    "unexpected constructor call inside a constructor call")
            commaCount = constructorParam.count(Comma())
            eqCount = constructorParam.count(Eq())
            if commaCount + 1 != eqCount or commaCount * 4 + 3 != len(constructorParam):
                raise ParseError(
                    "invalid constructor statements: %s" % constructorParam)
            while Comma() in constructorParam:
                comma = constructorParam.index(Comma())
                self.params.append(self.__generateParam(
                    constructorParam[:comma]))
                constructorParam = constructorParam[comma + 1:]
            self.params.append(self.__generateParam(constructorParam))
        [self.next() for i in range(move)]

    def __generateParam(self, tokenList):
        new_assign_node = AssignmentNode(tokenList)
        new_assign_node.parse()
        return new_assign_node

    def name_check(self):
        for param in self.params:
            param.name_check()

    def type_check(self, tk):
        if self.params:
            if tk.value == 'Nav':
                attr = self.default_nav_attr
                for param in self.params:
                    if param.var_name not in attr:
                        raise TypeCheckError(f"There is no such attribute called {param.var_name} in Nav component")
            elif tk.value == 'Header':
                attr = self.default_header_attr
                for param in self.params:
                    if param.var_name not in attr:
                        raise TypeCheckError(f"There is no such attribute called {param.var_name} in Header component")
            elif tk.value == 'Content':
                attr = self.default_content_attr
                for param in self.params:
                    if param.var_name not in attr:
                        raise TypeCheckError(f"There is no such attribute called {param.var_name} in Content component")
            elif tk.value == 'Link':
                attr = self.default_link_attr
                for param in self.params:
                    if param.var_name not in attr:
                        raise TypeCheckError(f"There is no such attribute called {param.var_name} in Link component")
            elif tk.value == 'Image':
                attr = self.default_image_attr
                for param in self.params:
                    if param.var_name not in attr:
                        raise TypeCheckError(f"There is no such attribute called {param.var_name} in Image component")
            elif tk.value == 'Video':
                attr = self.default_video_attr
                for param in self.params:
                    if param.var_name not in attr:
                        raise TypeCheckError(f"There is no such attribute called {param.var_name} in Video component")
            elif tk.value == 'Footer':
                attr = self.default_footer_attr
                for param in self.params:
                    if param.var_name not in attr:
                        raise TypeCheckError(f"There is no such attribute called {param.var_name} in Footer component")
            elif tk.value == 'Button':
                attr = self.default_button_attr
                for param in self.params:
                    if param.var_name not in attr:
                        raise TypeCheckError(f"There is no such attribute called {param.var_name} in Button component")
            elif tk.value == 'Page':
                attr = self.default_page_attr
                for param in self.params:
                    if param.var_name not in attr:
                        raise TypeCheckError(f"There is no such attribute called {param.var_name} in Page component")
            else:
                raise TypeCheckError(f"No such constructor called {tk.value}")


class LayoutNode(ASTNode):

    def parse(self):
        return super().parse()  # TODO

    def name_check(self):
        return  # TODO


class ParseError(Exception):
    def __init__(self, message):
        self.message = message


class NameCheckError(Exception):
    def __init__(self, message):
        message = "You didn't declare : " + message
        super().__init__(message)


class TypeCheckError(Exception):
    def __init__(self, message):
        self.message = message
