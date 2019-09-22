#!/bin/bash
set -e

echo "Adding githook --- not allowing commit if code coverage isn't above 80"
mv pre-commit .git/hooks/

if [ "$(which coverage)" -e "" ]; then
  echo "Install pip coverage"
  pip3 install coverage
fi

echo "Setup success"
