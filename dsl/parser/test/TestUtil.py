import os
import unittest
from ..ASTNode import *
from ...tokenizer.Token import *
from ...tokenizer.Tokenizer import Tokenizer

# Will log more detail
DEBUGGING = True if "DEBUG" in os.environ else False


class TestUtil(unittest.TestCase):
    # Sample usage:
    # @program  """
    #           abc = "123"
    #           """
    # @expect {
    #         'type': 'ProgramNode',
    #         'assignments': [
    #             {
    #                 'type': 'AssignmentNode',
    #                 'var_name': 'abc',
    #                 'assigned': "123"
    #             }
    #         ],
    #         'layouts': []
    #     }
    def expectPass(self, program, expect):
        pgNode = ProgramNode(self.tokenize(program))
        pgNode.parse()
        self.__validateNodes(pgNode, expect)

    def expectPassNameCheck(self, program):
        ASTNode.dereference_dict = {}
        pgNode = ProgramNode(self.tokenize(program))
        pgNode.parse()
        pgNode.name_check()

    def expectPassNameCheckWithEnv(self, program, expected_env):
        ASTNode.dereference_dict = {}
        pgNode = ProgramNode(self.tokenize(program))
        pgNode.parse()
        pgNode.name_check()
        self.__validateEnv(ASTNode.dereference_dict, expected_env)

    def expectFailNameCheck(self, program):
        ASTNode.dereference_dict = {}
        pgNode = ProgramNode(self.tokenize(program))
        pgNode.parse()

        try:
            pgNode.name_check()
            self.fail(
                "Failed --- unexpected name checking success for program %s" % program)
        except NameCheckError:
            pass

    def expectPassTypeCheck(self, program):
        ASTNode.dereference_dict = {}
        pgNode = ProgramNode(self.tokenize(program))
        pgNode.parse()
        pgNode.name_check()
        pgNode.type_check()

    def expectFailTypeCheck(self, program):
        ASTNode.dereference_dict = {}
        pgNode = ProgramNode(self.tokenize(program))
        pgNode.parse()
        pgNode.name_check()
        try:
            pgNode.type_check()
            self.fail(
                "Failed --- unexpected type checking success for program %s" % program)
        except TypeCheckError:
            pass

    def expectFail(self, program):
        try:
            if DEBUGGING:
                print("Testing %s" % program)
            pgNode = ProgramNode(self.tokenize(program))
            pgNode.parse()
            self.fail(
                "Failed --- unexpected parsing success for program %s" % program)
        except ParseError:
            pass

    def __validateEnv(self, env, expect):
        keys_in_env = list(env.keys())
        keys_in_expect = list(expect.keys())

        self.assertEqual(keys_in_env, keys_in_expect)
        for k in keys_in_env:
            expect_val = expect[k]
            actual_val = env[k]
            if isinstance(expect_val, dict):
                if not isinstance(actual_val, dict):
                    self.fail("not a dict in actual env")
                if not "constructor" in actual_val:
                    self.fail("missing constructor key in actual env")
                self.__validateNodes(actual_val["constructor"], expect_val["constructor"])

                if "layout" in expect_val:
                    if not "layout" in actual_val:
                        self.fail("missing layout")
                    self.__validateNodes(actual_val["layout"], expect_val["layout"])
            else:
                self.assertEqual(expect_val, actual_val)

    def __validateNodes(self, parsedNode, expect):
        for key in expect:
            if key == "type":
                # extract "ProgramNode" from "<class 'dsl.parser.ASTNode.ProgramNode'>"
                self.assertEqual(expect[key],
                                 str(parsedNode.__class__).split(".")[-1].replace("'>", ""))
            else:
                actualValue = parsedNode.__dict__[key]
                expectValue = expect[key]
                if DEBUGGING:
                    print("Validating node %s, expecting %s" %
                          (parsedNode, expect))
                    print("Expected value: %s, actual value: %s" %
                          (expectValue, actualValue))
                if type(expectValue) != dict:
                    self.assertEqual(type(expectValue),
                                    type(actualValue))
                if type(expectValue) is list:
                    self.assertEqual(type(actualValue), list)
                    self.assertEqual(len(expectValue), len(actualValue))
                    for i in range(len(expectValue)):
                        self.__validateNodes(actualValue[i], expectValue[i])
                elif type(expectValue) in [int, bool, str]:
                    self.assertEqual(expectValue, actualValue)
                else:
                    self.__validateNodes(actualValue, expectValue)

    def tokenize(self, str):
        return Tokenizer().read(str)
