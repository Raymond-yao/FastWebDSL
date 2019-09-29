import unittest
from dsl.test.TestUtil import *


class ConstructorNodeSpec(TestUtil):
    def test_invalid_syntax_quick_check(self):
        programs = [
            "A",
            "a a =",
            " = A",
            " = A(",
            " = A()",
            " = A)",
            "a = ",
            "a = A()",  # not a valid func
            "a = Nav(",
            "a = Nav)",
            "a = Nav(  page {} )",
            "a = Nav( wrong )",
            "a = Nav(a=)",
            "a = Nav(a=1,)",
            "a = Nav(a=1,a=1,)",
            "a = Nav(a=1,a=1 page{haha})",
            "a = Nav(()())",
            "a = Nav(()",
            "a = Nav((),())",
            "a = Nav(a=())",
            "a = Nav(a=Nav())",
            "a = Nav(a=Nav)"
        ]
        for program in programs:
            self.expectFail(program)

    def test_constructor_without_param(self):
        program = """
            test = Nav()
        """
        self.expectPass(program, {
            'type': 'ProgramNode',
            'assignments': [
                {
                    'type': 'AssignmentNode',
                    'var_name': 'test',
                    'assignment_type': 'FUNC',
                    'assigned': {
                        'type': "ConstructorNode",
                        'params': []
                    }
                }
            ]
        })

    def test_constructor_with_param(self):
        program = """
            test = Nav(a=1, b=haha, c="test")
        """
        self.expectPass(program, {
            'type': 'ProgramNode',
            'assignments': [
                {
                    'type': 'AssignmentNode',
                    'var_name': 'test',
                    'assignment_type': 'FUNC',
                    'assigned': {
                        'type': 'ConstructorNode',
                        'params': [
                            {
                                'type': 'AssignmentNode',
                                'var_name': 'a',
                                'assigned': 1,
                                'assignment_type': 'NUM'
                            },
                            {
                                'type': 'AssignmentNode',
                                'var_name': 'b',
                                'assigned': 'haha',
                                'assignment_type': 'VAR'
                            },
                            {
                                'type': 'AssignmentNode',
                                'var_name': 'c',
                                'assigned': 'test',
                                'assignment_type': 'STRING'
                            }
                        ]
                    }
                }
            ]
        })

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
