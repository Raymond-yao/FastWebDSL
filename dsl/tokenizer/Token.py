from enum import Enum
from ..interpreter.components.ComponentFactory import ALL_COMPONENTS

"""
    An enumeration of tokens
    NOTE:
    RESERVED = Nav | Header | Content | Link | Image | Video | Footer | Button | Page
    VARIABLE includes Attribute name and Variable name
        e.g. Nav(size="small"), size is an IDENTIFIER
             newNav = Nav(size="small"), newNav is an IDENTIFIER
"""


class Type(Enum):
    STRING = 1
    NUMBER = 2
    END = 3
    RESERVED = 4
    VARIABLE = 5
    BRACKET = 6
    EQUAL = 7
    COMMA = 8


RESERVED_NAME = set(ALL_COMPONENTS.keys())


class Token:

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Token):
            return NotImplemented
        else:
            return self.type == other.type and self.value == other.value

    def __repr__(self):
        return f"{self.type.name}('{self.value}')"

    def is_a(self, tpe):
        return self.type == tpe


class InvalidTokenError(Exception):
    def __init__(self, message):
        self.message = message


'''
    Helper constructors, you can always use the default Token() if you want
'''


def Str(val):
    return Token(Type.STRING, val)


def Num(val):
    return Token(Type.NUMBER, val)

def Reserved(val):
    return Token(Type.RESERVED, val)


def Var(val):
    return Token(Type.VARIABLE, val)


def Bracket(val):
    return Token(Type.BRACKET, val)


def Eq():
    return Token(Type.EQUAL, "=")


def Comma():
    return Token(Type.COMMA, ",")
