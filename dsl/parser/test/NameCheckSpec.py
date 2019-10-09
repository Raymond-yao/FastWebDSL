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

    def test_name_check_fail_complex(self):
        program = """
                some_num = 1
                some_str = "2"
                some_var = some_num
                some_var2 = some_str
                nav = Nav(size=a)
                """
        self.expectFailNameCheck(program)


if __name__ == '__main__':
    unittest.main()
