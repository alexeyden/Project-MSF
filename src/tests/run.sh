#!/bin/bash

export PYTHONPATH=$PYTHONPATH:`realpath ..`

failed=()

for x in *_test.py; do
    echo "Running $x:"

    python3 $x -v

    if [[ $? != 0 ]]; then
        failed[${#failed[*]}]=$x
    fi
done

if [[ ${#failed[*]} == 0 ]]; then
    echo -e "\033[32mAll tests passed\033[0m"
else
    echo -e "\033[31m${#failed[*]} test(s) failed:\033[0m"

    for x in ${failed[*]}; do
        echo "  $x"
    done
fi