#!/bin/bash
set -e

echo "-------- Executing Tests Before Commit --------"
echo ""
echo "-------- Tokenizer Tests --------"
coverage run -m dsl.tokenizer.test.TokenizerSpec
echo ""
echo "-------- Parser Tests --------"
coverage run -m dsl.parser.test.ASTNodeSpec
coverage run -m dsl.parser.test.ConstructorNodeSpec
coverage run -m dsl.parser.test.LayoutNodeSpec
coverage run -m dsl.parser.test.NameCheckSpec
coverage run -m dsl.parser.test.TypeCheckSpec
coverage run -m dsl.interpreter.test.InterpreterSpec

coverage report
TEMP=$(coverage report | grep "TOTAL" | awk '{print $4}')
COVERAGE=$(echo "${TEMP/\%/$NON_EXIST}")
CODE=$(test $COVERAGE -ge 60)
exit $CODE
