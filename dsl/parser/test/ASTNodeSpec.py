import unittest
from ..ASTNode import *
from ...tokenizer.Token import *

class ASTNodeSpec(unittest.TestCase):

    def test_ProgramNode_invalid(self):
        invalids = [[Eq()], [Num(123)], [Str("123")], [Comma()], [Bracket("(")]]
        for invalid_p in invalids:
            self.assertRaises(ParseError, ProgramNode(invalid_p).parse)

    def test_ProgramNode_normal(self):
        tk_list = [NewLine(), NewLine(), NewLine(), Var("abc"), Eq(), Str("123")]
        pgNode = ProgramNode(tk_list)
        pgNode.parse()
        self.assertEqual(len(pgNode.assignments), 1)
        self.assertEqual(len(pgNode.layouts), 0)
        self.assertEqual(len(pgNode.assignments), 1)
        self.assertEqual(pgNode.assignments[0].assignment_type, AssignmentNode.STRING)
        self.assertEqual(pgNode.assignments[0].assigned, "123")



if __name__ == '__main__':
    unittest.main()
