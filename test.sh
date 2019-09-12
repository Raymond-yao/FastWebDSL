#!/bin/bash
set -e

echo "-------- Executing Tests Before Commit --------"
echo ""
echo "-------- Tokenizer Tests --------"
python3 -m tokenizer.test.TokenizerSpec

