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

if __name__ == '__main__':
    unittest.main()
