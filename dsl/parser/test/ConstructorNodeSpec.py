import unittest
from .TestUtil import *


class ConstructorNodeSpec(TestUtil):
    def test_assignment_node_complex(self):
        program = """
                some_num = 1
                some_str = "2"


                some_var = var1

                """
        self.expectPass(program, {
            'type': 'ProgramNode',
            'assignments': [
                {
                    'type': 'AssignmentNode',
                    'var_name': 'some_num',
                    'assigned': 1
                }, {
                    'type': 'AssignmentNode',
                    'var_name': 'some_str',
                    'assigned': "2"
                }, {
                    'type': 'AssignmentNode',
                    'var_name': 'some_var',
                    'assigned': "var1"
                },
            ],
            'layouts': []
        })

    def test_assignment_node_invalid(self):
        program = "a = \n"
        self.expectFail(program)


if __name__ == '__main__':
    unittest.main()
