import unittest
from ..Interpreter import *
from ...tokenizer.Tokenizer import tokenize
from ...parser.ASTNode import parse, check
from ..test.InterpTestHelper import TestFactory

class InterpreterSpec(unittest.TestCase):
    def test_interp(self):
        program = """ 
            text = "Hello World!"
            l1 = text
            l2 = l1
            middle = text

            my_header = Header(size=100, colour="black")
            my_header {
                [l1 text l2]
            }

            button_1 = Link()
            button_2 = Link()

            my_nav = Nav(size=200, colour="blue")
            my_nav {
                [button_1]
                [button_2]
            }

            Page {
                [my_header]
                [my_nav]
            }
        """
        result = Interpreter(check(parse(tokenize(program))), TestFactory()).interp()
        self.assertEqual(result, {
            "name": "Page",
            "params": {},
            "rows": [
                [{
                    "name": "Header",
                    "params": {
                        "size": 100,
                        "colour": "black",
                        'title': 'Navigation'
                    },
                    "rows": [[
                        {"name": "Text","params": {"text": "Hello World!"},"rows": []},
                        {"name": "Text","params": {"text": "Hello World!"},"rows": []},
                        {"name": "Text","params": {"text": "Hello World!"},"rows": []}
                        ]]
                }],
                [{
                    "name": "Nav",
                    "params": {
                        "size": 200,
                        "colour": "blue"
                    },
                    "rows": [
                        [{"name": "Link", "params": {'ref': '', 'colour': 'black', 'title': 'Navigation'}, "rows": []}],
                        [{"name": "Link", "params": {'ref': '', 'colour': 'black', 'title': 'Navigation'}, "rows": []}]
                    ]
                }]
            ]
        })

if __name__ == '__main__':
    unittest.main()
