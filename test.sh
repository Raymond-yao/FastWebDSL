#!/bin/bash
set -e

echo "-------- Executing Tests Before Commit --------"
echo ""
echo "-------- Tokenizer Tests --------"
python3 -m dsl.tokenizer.test.TokenizerSpec
echo ""
echo "-------- Parser Tests --------"
python3 -m dsl.parser.test.ASTNodeSpec
python3 -m dsl.parser.test.ConstructorNodeSpec

