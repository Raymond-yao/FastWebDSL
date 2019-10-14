import argparse
import os
import shutil
import subprocess
import sys
import time

from dsl.tokenizer.Tokenizer import tokenize
from dsl.parser.ASTNode import parse
from dsl.interpreter.Interpreter import check, evaluate

DSL_PREFIX = "Fast-Web-DSL"
REACT_SOURCE_PATH = "dsl/build/react-template/"
TEMPLATE_PATH = REACT_SOURCE_PATH + "src/App-Template.js"
REACT_APP_PATH = REACT_SOURCE_PATH + "src/App.js"
REACT_BUILD_PATH = "dsl/build/react-template/build"
OUTPUT_PATH = "out/"


def main():
    outputName = DSL_PREFIX + str(int(time.time()))
    description = """
    Fast Web DSL uses a declarative syntax to help you quickly generate an HTML template!
    All you need to do is to specify your layout structure and customize our pre-defined
    components.
    Please refer to https://github.com/Raymond-yao/FastWebDSL
    """
    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.RawDescriptionHelpFormatter,)
    parser.add_argument("path", metavar="DSL path",
                        type=str, help="path to your DSL code")
    parser.add_argument("-d", "--dev", action="store_true",
                        help="will only generate a dev version of the react project")
    parser.add_argument("-n", "--name", type=str, default=outputName,
                        help="name of your generated dsl project")
    parser.add_argument("-o", "--out", type=str, default=OUTPUT_PATH,
                        help="path to your generated dsl project")
    args = parser.parse_args()

    if not os.path.exists(args.path):
        raise Exception("Please specify a valid path to your DSL code")

    with open(args.path) as f:
        program = f.read()

    print("Compiling Your Fast Web DSL...")
    reactComponet = evaluate(check(parse(tokenize(program))))
    print("Success! Generating React Project...")
    with open(TEMPLATE_PATH) as f:
        template = f.read()
    with open(REACT_APP_PATH, "w+") as f:
        f.write(template + reactComponet)
    if args.dev:
        print("Packing Your Dev React Project")
        shutil.make_archive(OUTPUT_PATH + "dev-" + outputName, "zip", REACT_SOURCE_PATH)
        print("Done!")
    else:
        print("Building Your React Project")
        root = os.getcwd()
        os.chdir(REACT_SOURCE_PATH)
        subprocess.run(["npm", "install"])
        subprocess.run(["npm", "run", "build"])
        subprocess.run(["rm", "-rf", "node_modules"])
        os.chdir(root)
        shutil.make_archive(OUTPUT_PATH + outputName, "zip", REACT_BUILD_PATH)
        subprocess.run(["rm", "-rf", REACT_BUILD_PATH])

main()
