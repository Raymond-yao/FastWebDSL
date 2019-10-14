import os.path
import sys

from dsl.tokenizer.Tokenizer import tokenize
from dsl.parser.ASTNode import parse
from dsl.interpreter.Interpreter import check, evaluate


def main(program):
    reactComponet = evaluate(check(parse(tokenize(program))))


if len(sys.argv) != 2:
    raise Exception("Please specify a path to your DSL code")

path = sys.argv[1]
if not os.path.exists(path):
    raise Exception("Please specify a valid path to your DSL code")

with open(path) as f:
    content = f.read()

main(content)


if __name__ == "__main__":
    program = """ 

    
    
    """

    jsx = evaluate(
        check(
            parse(
                tokenize(
                    program))))
    print(jsx)
