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
        pgNode = ProgramNode(self.tokenize(program))
        pgNode.parse()
        pgNode.name_check()

    def expectFailNameCheck(self, program):
        pgNode = ProgramNode(self.tokenize(program))
        pgNode.parse()

        try:
            pgNode.name_check()
            self.fail(
                "Failed --- unexpected name checking success for program %s" % program)
        except NameCheckError:
            pass

    def expectPassTypeCheck(self, program):
        pgNode = ProgramNode(self.tokenize(program))
        pgNode.parse()
        pgNode.name_check()
        pgNode.type_check()

    def expectFailTypeCheck(self, program):
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
