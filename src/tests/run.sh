#!/bin/bash

export PYTHONPATH=$PYTHONPATH:`realpath ..`

for x in *.py; do
    python3 $x -v
done