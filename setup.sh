#!/bin/bash
set -e

echo "Adding githook --- not allowing commit if code coverage isn't above 80"
cp pre-commit .git/hooks/

echo "Install pip coverage"
pip3 install coverage

echo "Setup success"
