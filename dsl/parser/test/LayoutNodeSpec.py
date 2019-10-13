import unittest
from .TestUtil import *

class LayoutNodeSpec(TestUtil):
    def test_layout_with_one_element_row(self):
        program = """
            Page {
                [Header()]
            }
        """
        self.expectPass(program, {
        'type': 'ProgramNode',
        'assignments': [],
        'layouts': [
            {
                'type': 'LayoutNode',
                'layoutName': 'Page',
                'rows':[
                    {
                        'type': 'RowNode',
                        'elements': [
                            {
                                'type': 'ConstructorNode',
                                'params':[]
                            }
                        ]
                    }
                ]
            }
        ]
        })

    def test_layout_with_multiple_elements_row(self):
        program = """
            Page {
                [Header() Nav() Header()]
            }
        """
        self.expectPass(program, {
        'type': 'ProgramNode',
        'assignments': [],
        'layouts': [
            {
                'type': 'LayoutNode',
                'layoutName': 'Page',
                'rows':[
                    {
                        'type': 'RowNode',
                        'elements': [
                            {
                                'type': 'ConstructorNode',
                                'params':[]
                            },
                            {
                                'type': 'ConstructorNode',
                                'params':[]
                            },
                            {
                                'type': 'ConstructorNode',
                                'params':[]
                            }
                        ]
                    }
                ]
            }
        ]
        })

    def test_layout_with_multiple_rows(self):
        program = """
            Page {
                [Header()]
                [nav1 main]
                [Footer()]
            }
        """
        self.expectPass(program, {
        'type': 'ProgramNode',
        'assignments': [],
        'layouts': [
            {
                'type': 'LayoutNode',
                'layoutName': 'Page',
                'rows':[
                    {
                        'type': 'RowNode',
                        'elements': [
                            {
                                'type': 'ConstructorNode',
                                'params':[]
                            }
                        ]
                    },
                    {
                        'type': 'RowNode',
                        'elements': [
                            {
                                'type': 'VarNode',
                                'varName': 'nav1'
                            },
                            {
                                'type': 'VarNode',
                                'varName': 'main'
                            }
                        ]
                    },
                    {
                        'type': 'RowNode',
                        'elements': [
                            {
                                'type': 'ConstructorNode',
                                'params':[]
                            }
                        ]
                    }
                ]
            }
        ]
        })

    def test_layout_with_variable_name(self):
        program = """
            Page {
                [new_nav]
            }
            new_nav {
                [Link()]
            }
        """
        self.expectPass(program, {
        'type': 'ProgramNode',
        'assignments': [],
        'layouts': [
            {
                'type': 'LayoutNode',
                'layoutName': 'Page',
                'rows':[
                    {
                        'type': 'RowNode',
                        'elements': [
                            {
                                'type': 'VarNode'
                            }
                        ]
                    }
                ]
            },
            {
                'type': 'LayoutNode',
                'layoutName': 'new_nav',
                'rows':[
                    {
                        'type': 'RowNode',
                        'elements': [
                            {
                                'type': 'ConstructorNode',
                                'params':[]
                            }
                        ]
                    }
                ]
            }
        ]
        })

    def test_layout_missing_page(self):
        program = """
            {
                [Header()]
            }
        """
        self.expectFail(program)

    def test_layout_missing_lbrace(self):
        program = """
            Page
                [Header()]
            }
        """
        self.expectFail(program)

    def test_layout_missing_rbrace(self):
        program = """
            Page {
                [Header()]

        """
        self.expectFail(program)

    def test_invalid_element(self):
        program = """
            Page {
                [Header() 123]
            }
        """
        self.expectFail(program)

    def test_missing_page(self):
        program = """ 
            unknown {
                ["123"]
            }
        """
        self.expectPass(program, {
        'type': 'ProgramNode',
        'assignments': [],
        'layouts': [
            {
                'type': 'LayoutNode',
                'layoutName': 'unknown',
                'rows':[
                    {
                        'type': 'RowNode',
                        'elements': [
                            {
                                'type': 'ConstructorNode',
                                'constructor_name': "Text",
                                "params": [
                                    {'type': "AssignmentNode", "assignment_type": "STRING", "var_name": "text", "assigned": '123'}
                                ]
                            }
                        ]
                    }
                ]
            }]})
if __name__ == '__main__':
    unittest.main()
