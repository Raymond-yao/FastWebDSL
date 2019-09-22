#!/bin/bash
set -e

if [ "$(which coverage)" -e "" ]; then
  echo "Please install pip coverage first"
  pip3 install coverage
fi

echo "-------- Executing Tests Before Commit --------"
echo ""
echo "-------- Tokenizer Tests --------"
coverage run -m dsl.tokenizer.test.TokenizerSpec
echo ""
echo "-------- Parser Tests --------"
coverage run -m dsl.parser.test.ASTNodeSpec
coverage run -m dsl.parser.test.ConstructorNodeSpec

coverage report
TEMP=$(coverage report | grep "TOTAL" | awk '{print $4}')
COVERAGE=$(echo "${TEMP/\%/$NON_EXIST}")
CODE=$(test $COVERAGE -ge 80)
exit $CODE
