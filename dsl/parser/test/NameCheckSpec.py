import unittest
from dsl.parser.test.TestUtil import TestUtil


class NameCheckSpec(TestUtil):
    def test_name_check_pass(self):
        program = """
                some_num = 1
                some_str = "2"
                some_var = some_num
                some_var2 = some_str
                """
        self.expectPassNameCheck(program)

    def test_name_check_fail(self):
        program = """
                some_num = 1
                some_str = "2"
                some_var = a
                some_var2 = b
                """
        self.expectFailNameCheck(program)

    def test_name_check_pass_complex(self):
        program = """
                some_num = 1
                some_str = "2"
                some_var = some_num
                some_var2 = some_str
                nav = Nav(size=some_var)
                """
        self.expectPassNameCheck(program)

    def test_name_check_pass_very_complex(self):
        program = """
                a = 1
                b = a
                c = b
                d = c
                e = d
                nav = Nav(size=e)
                """
        self.expectPassNameCheck(program)

    def test_name_check_fail_complex(self):
        program = """
                some_num = 1
                some_str = "2"
                some_var = some_num
                some_var2 = some_str
                nav = Nav(size=a)
                """
        self.expectFailNameCheck(program)

    def test_name_check_fail_layout1(self):
        program = """ 
            unknown_var {
                ["123"]
            }
        """
        self.expectFailNameCheck(program)

    def test_name_check_fail_layout2(self):
        program = """
            new_nav = Nav()
            new_nav {
                [unknown_var]
            }
        """
        self.expectFailNameCheck(program)

    def test_name_check_fail_layout3(self):
        program = """
            new_nav = Nav()
            new_header = Header()

            new_header {
                [unknown_var]
            }

            new_nav {
                [new_header]
            }
        """
        self.expectFailNameCheck(program)

    def test_name_check_good_layout(self):
        program = """
            some_text = "hello"
            new_header = Header()
            new_nav = Nav()
            some_content = Content()

            Page {
                [new_header]
                [new_nav some_content new_nav]
                [new_header "123"]
            }

            new_header {
                [Nav() Nav() Nav() some_text new_nav]
            }

            new_nav {
                [some_text some_text some_text]
            }
        """
        self.expectPassNameCheckWithEnv(program, {
            'some_text': 'hello', 
            'new_header': {
                'constructor': {
                    'type': 'ConstructorNode',
                    'constructor_name': 'Header',
                    'params': []
                }, 
                'layout': {
                    'type': 'LayoutNode',
                    'layoutName': 'new_header',
                    'rows': [
                        {
                            'type': 'RowNode',
                            'elements': [
                                {'type': 'ConstructorNode', 'constructor_name': 'Nav', 'params': []},
                                {'type': 'ConstructorNode', 'constructor_name': 'Nav', 'params': []},
                                {'type': 'ConstructorNode', 'constructor_name': 'Nav', 'params': []},
                                {'type': 'VarNode', 'varName': "some_text"},
                                {'type': 'VarNode', 'varName': "new_nav"}
                            ]
                        }
                    ]
                }
            }, 
            'new_nav': {
                'constructor': {
                    'type': 'ConstructorNode',
                    'constructor_name': 'Nav',
                    'params': []
                }, 
                'layout': {
                    'type': 'LayoutNode',
                    'layoutName': 'new_nav',
                    'rows': [
                        {
                            'type': 'RowNode',
                            'elements': [
                                {'type': 'VarNode','varName': 'some_text'},
                                {'type': 'VarNode', 'varName': 'some_text'},
                                {'type': 'VarNode','varName': 'some_text'}
                            ]
                        }
                    ]
                }
            }, 
            'some_content': {
                'constructor': {
                    'type': 'ConstructorNode',
                    'constructor_name': 'Content',
                    'params': []
                }
            }
        })

        def test_type_check_fail_layout(self):
            """ 
                it's kinda mixed here since this is a typecheck, but we need to do typecheck first for layout since
                it does not make sense to add a layout to a string/number variable
            """
            program = """ 
                text = "123"

                text {
                    ["123"]
                }
            """
            self.expectFailTypeCheck(program)


    def test_another_name_check_good_layout(self):
        program = """ 
            text = "Hello World!"
            l1 = text
            l2 = l1
            middle = text

            my_header = Header()
            my_header {
                [l1 text l2]
            }

            button_1 = Link()
            button_2 = Link()

            my_nav = Nav(size=100)
            my_nav {
                [button_1]
                [button_2]
            }

            Page {
                [my_header]
                [my_nav]
            }
        """
        self.expectPassNameCheckWithEnv(program, {
            'text': "Hello World!",
            'l1': "Hello World!",
            'l2': "Hello World!",
            'middle': "Hello World!",
            'my_header': {
                'constructor': {'type': "ConstructorNode", "constructor_name": "Header", "params": []},
                "layout": {'type': "LayoutNode", "layoutName": "my_header", 
                    "rows": [
                        {'type': "RowNode", 'elements': [
                            {'type': 'VarNode', 'varName': "l1"},
                            {'type': 'VarNode', 'varName': "text"},
                            {'type': 'VarNode', 'varName': "l2"}
                        ]}
                    ]
                }
            },
            'button_1': {
                'constructor': {'type': "ConstructorNode", "constructor_name": "Link", "params": []}
            },
            "button_2": {
                'constructor': {'type': "ConstructorNode", "constructor_name": "Link", "params": []}
            },
            'my_nav': {
                'constructor': {'type': "ConstructorNode", "constructor_name": "Nav", "params": [
                    {
                        'type': "AssignmentNode",
                        'var_name': 'size',
                        "assigned": 100
                    }
                ]},
                'layout': {
                    'type': "LayoutNode", 
                    "layoutName": "my_nav", 
                    "rows": [
                        {'type': "RowNode", 'elements': [
                            {'type': 'VarNode', 'varName': "button_1"},
                        ]},
                        {'type': "RowNode", 'elements': [
                            {'type': 'VarNode', 'varName': "button_2"}
                        ]}
                    ]
                }
            }
        })

if __name__ == '__main__':
    unittest.main()
