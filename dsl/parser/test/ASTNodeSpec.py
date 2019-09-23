import unittest
from ..ASTNode import *
from ...tokenizer.Token import *
from ...tokenizer.Tokenizer import Tokenizer
from .TestUtil import *

class ASTNodeSpec(unittest.TestCase):

    def tokenize(self, str):
        return Tokenizer().read(str)

    def test_ProgramNode_invalid(self):
        invalids = [[Eq()], [Num(123)], [Str("123")], [Comma()], [Bracket("(")]]
        for invalid_p in invalids:
            self.assertRaises(ParseError, ProgramNode(invalid_p).parse)

    def test_ProgramNode_normal(self):
        program = """

            abc = "123"

        """
        pgNode = ProgramNode(self.tokenize(program))
        pgNode.parse()
        self.assertEqual(self.structurize(pgNode), {
            'type': 'ProgramNode',
            'assignments': [
                {
                    'type': 'AssignmentNode',
                    'var_name': 'abc',
                    'assigned': "123"
                }
            ],
            'layouts': []
        })

    def test_multiple_simple_assignments(self):
        program = """
        
        some_num = 1
        some_str = "2"
        
        
        some_var = var1
        
        """
        pgNode = ProgramNode(self.tokenize(program))
        pgNode.parse()
        self.maxDiff = None
        self.assertEqual(self.structurize(pgNode), {
            'type': 'ProgramNode',
            'assignments': [
                {
                    'type': 'AssignmentNode',
                    'var_name': 'some_num',
                    'assigned': 1
                },{
                    'type': 'AssignmentNode',
                    'var_name': 'some_str',
                    'assigned': "2"
                },{
                    'type': 'AssignmentNode',
                    'var_name': 'some_var',
                    'assigned': "var1"
                },
            ],
            'layouts': []
        })

    def structurize(self, node):
        """
            A recursive helper to dump an AST tree to a nested dictionary object
            one can also call json.dump to move it to a json.
        """
        if isinstance(node, ProgramNode):
            assign_arr = []
            layout_arr = []
            for a in node.assignments:
                assign_arr.append(self.structurize(a))
            for l in node.layouts:
                layout_arr.append(self.structurize(l))
            return {
                'type': 'ProgramNode',
                'assignments': assign_arr,
                'layouts': layout_arr
            }
        elif isinstance(node, AssignmentNode):
            if node.assignment_type == AssignmentNode.FUNC:
                return {
                    'type': 'AssignmentNode',
                    'var_name': node.var_name,
                    'assigned': structurize(node.assigned)
                }
            else:
                 return {
                    'type': 'AssignmentNode',
                    'var_name': node.var_name,
                    'assigned': node.assigned
                }
        else: 
            return {}
            

if __name__ == '__main__':
    unittest.main()
