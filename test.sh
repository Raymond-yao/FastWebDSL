#!/bin/bash
set -e

# Test script for validating functionality and code coverage

calculateCoverage() {
    echo "-------- Runing $1 $2 Test --------"
    coverage run -m "dsl.$1.test.$2"
    coverage report
}

echo "-------- Executing Tests Before Commit --------"

# Note: Test modules --- Please make sure actual tests are named with "*Spec.py"
MODULES=("tokenizer" "parser" "interpreter")
for MODULE in "tokenizer" "parser" "interpreter"; do
    SPECS=$(ls dsl/$MODULE/test/ | grep "Spec" | awk -F '.' '{print $1}')
    for SPEC in $SPECS; do
        calculateCoverage $MODULE $SPEC
    done;
done
