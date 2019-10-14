import unittest
from dsl.parser.test.TestUtil import TestUtil


class TypeCheckSpec(TestUtil):
    def test_type_check_pass_attr_type(self):
        program = """
                a = Nav()
                b = Nav(size=1)
                """
        self.expectPassTypeCheck(program)

    def test_type_check_fail_attr_type(self):
        program = """
                a = Nav(size="")
                """
        self.expectFailTypeCheck(program)

    def test_type_check_pass_attr_name(self):
        program = """
                a = Nav(b=1)
                """
        self.expectFailTypeCheck(program)

    def test_type_check_pass_complex(self):
        program = """
                some_num = 1
                some_str = "2"
                some_var = some_num
                some_var2 = some_str
                a = Nav(size = some_var, colour = some_var2)
                """
        self.expectPassTypeCheck(program)

    def test_type_check_fail_multiple_declaration(self):
        program = """
                a = 1
                b = "black"
                nav = Nav(size = a, size = a)
                """
        self.expectFailTypeCheck(program)

    def test_type_check_fail_multiple_declaration_complex(self):
        program = """
                nav = Nav(size = 1, colour = "black")
                nav2 = Nav(size = 1, colour = "black", size = 2)
                """
        self.expectFailTypeCheck(program)



