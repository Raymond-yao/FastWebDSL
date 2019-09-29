#!/bin/bash

# Test modules --- Please make sure the new test files named "*Spec.py"
MODULES=$(ls dsl/test/ | grep "Spec" | awk -F '.' '{print $1}')
# Threshold for test coverage
THRESHOLD=82

echo "-------- Executing Tests Before Commit --------"

calculateCoverage() {
    echo "-------- Runing $1 Test --------"
    coverage run -m "dsl.test.$1"
    coverage report
    TEMP=$(coverage report | grep "TOTAL" | awk '{print $4}')
    COVERAGE=$(echo "${TEMP/\%/$NON_EXIST}")
    return $COVERAGE
}

COUNT=0
COVERAGE=0
for MODULE in $MODULES; do
    calculateCoverage $MODULE
    ((COVERAGE+=$?))
    ((COUNT++))
done

if [ $COVERAGE -le $(( COUNT*THRESHOLD )) ]; then
  echo "Current test coverage $COVERAGE out of $(( COUNT*100 )) did NOT meet
the coverage threashold $(( COUNT*THRESHOLD )) out of $(( COUNT*100 ))!"
  echo "Please add more tests to validate functionality!"
  exit 1
fi
