#!/bin/bash
set -e

echo "Building sample/demo_dsl"
python3 run.py sample/demo_dsl

echo "Extracting the generated project"
cd "sample_output"
name=$(ls -t | head -n1 | awk -F '[.]' '{print $1;}')
unzip "$name.zip" -d $name

echo "Hosting the generated project at http://localhost:8000"
cd $name
python3 -m http.server 8000
