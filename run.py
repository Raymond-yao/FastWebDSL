from dsl.tokenizer.Tokenizer import *
from dsl.parser.ASTNode import *
from dsl.interpreter.components import *
from dsl.interpreter.Interpreter import *

if __name__ == "__main__":
    program = """ 
        new_nav = Nav()
        new_content = Content()
        new_content {
            ["123"]
            [new_nav]
        }

        Page {
            [Header()]
            [Nav() new_content new_nav]
        }
    
    
    """

    
    jsx = evaluate(
            check(
                parse(
                    tokenize(
                        program))))
    print(jsx)