import unittest
from ..Tokenizer import Tokenizer
from ..Token import *


class TokenizerSpec(unittest.TestCase):

    def test_spaces(self):
        tk = Tokenizer()
        program = "                  "
        self.assertEqual(tk.read(program), [])

    def test_new_line(self):
        tk = Tokenizer()
        program = "\n\n\n\n\n\n\n\n\n"
        self.assertEqual(tk.read(program), [NewLine(), NewLine(), NewLine(
        ), NewLine(), NewLine(), NewLine(), NewLine(), NewLine(), NewLine()])
        program = """


        """
        self.assertEqual(tk.read(program), [NewLine(), NewLine(), NewLine()])

    def test_string(self):
        tk = Tokenizer()
        program = """ "qwertyuiop[]" """
        self.assertEqual(tk.read(program), [Str("qwertyuiop[]")])

    def test_number(self):
        tk = Tokenizer()
        program = "123"
        self.assertEqual(tk.read(program), [Num(123)])

    def test_brackets(self):
        tk = Tokenizer()
        program = "{(}){)}(()()(){}}"

        expected_res = []
        for br in program:
            expected_res.append(Bracket(br))

        self.assertEqual(tk.read(program), expected_res)

    def test_eq(self):
        tk = Tokenizer()
        program = "======="
        expect = []
        for eq in program:
            expect.append(Eq())
        self.assertEqual(tk.read(program), expect)

    def test_comma(self):
        tk = Tokenizer()
        program = ",,,"
        self.assertEqual(tk.read(program), [Comma(), Comma(), Comma()])

    def test_function_name(self):
        tk = Tokenizer()
        programs = ["Nav", "Header", "Content", "Link",
                    "Image", "Video", "Footer", "Button", "Page"]
        for func_name in programs:
            self.assertEqual(tk.read(func_name), [Reserved(func_name)])

    def test_variable(self):
        tk = Tokenizer()
        program = ["navBar1", "this_can_be_var",
                   "another_navBar1", "nav2add", "CoolNavBar"]
        expect = []
        for var_name in program:
            expect.append(Var(var_name))
        self.assertEqual(tk.read(" ".join(program)), expect)

    def test_function_assignment_mul_lines(self):
        tk = Tokenizer()
        program = """ cool_nav_bar = Nav(
                        size= "small",
                        colour = "blue",
                        capacity     =    9999999
                      )"""
        self.assertEqual(tk.read(program), [
            Var("cool_nav_bar"), Eq(), Reserved(
                "Nav"), Bracket("("), NewLine(),
            Var("size"), Eq(), Str("small"), Comma(), NewLine(),
            Var("colour"), Eq(), Str("blue"), Comma(), NewLine(),
            Var("capacity"), Eq(), Num(9999999), NewLine(),
            Bracket(")")
        ])

    def test_function_assignment_one_line(self):
        tk = Tokenizer()
        program = """newLink=Link("https://ubc.ca")"""
        self.assertEqual(tk.read(program), [
            Var("newLink"), Eq(), Reserved("Link"), Bracket(
                "("), Str("https://ubc.ca"), Bracket(")")
        ])

    def test_constant_assignment(self):
        tk = Tokenizer()
        program = """expected_text=                      "this is a text" """
        self.assertEqual(tk.read(program), [Var(
            "expected_text"), Eq(), Str("this is a text")])

    def test_layout_mul_lines(self):
        tk = Tokenizer()
        program = """ Page{
                        Header
                        Nav Content custom_Nav
                        FancyFooter_self_made
                        Footer
                      }"""
        self.assertEqual(tk.read(program), [
            Reserved("Page"), Bracket("{"), NewLine(),
            Reserved("Header"), NewLine(),
            Reserved("Nav"), Reserved("Content"), Var("custom_Nav"), NewLine(),
            Var("FancyFooter_self_made"), NewLine(),
            Reserved("Footer"), NewLine(),
            Bracket("}")
        ])

    def test_string_number_combination(self):
        tk = Tokenizer()
        program = """
            234 "abc" "def" 2444 "aaa" "123" 321 "244"
            "raymondchen" 25555 6777 7888 8999 "abcdefg" "abcdefge"
            "fffghjk"
        """
        self.assertEqual(tk.read(program), [NewLine(),
                                            Num(234), Str("abc"), Str("def"), Num(2444), Str(
                                                "aaa"), Str("123"), Num(321), Str("244"), NewLine(),
                                            Str("raymondchen"), Num(25555), Num(6777), Num(7888), Num(
            8999), Str("abcdefg"), Str("abcdefge"), NewLine(),
            Str("fffghjk"), NewLine()
        ])

    def test_number_with_brackets_followed(self):
        tk = Tokenizer()
        programs = {
            ")": "123)",
            "}": "123}"
        }
        for k, v in programs.items():
            self.assertEqual(tk.read(v), [Num(123), Bracket(k)])

    def test_string_error(self):
        tk = Tokenizer()
        programs = [""" "abc123""", """ "abc\n" """]
        for invalid_p in programs:
            try:
                tk.read(invalid_p)
                self.fail("should throw InvalidTokenError")
            except InvalidTokenError as err:
                pass

    def test_number_error(self):
        tk = Tokenizer()
        programs = [""" 1234"abc """, """ 12"3 """, """ 1234"abc" """, "1234a"]
        for invalid_p in programs:
            try:
                tk.read(invalid_p)
                self.fail("should throw InvalidTokenError")
            except InvalidTokenError as err:
                pass


if __name__ == '__main__':
    unittest.main()
