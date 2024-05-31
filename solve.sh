#!/bin/bash

# Check if exactly one argument is provided
if [ "$#" -ne 1 ]; then
  echo "Error: Exactly one argument is required."
  exit 1
fi

input_program=$1
# Check if the argument is a valid path to a file
if [ ! -f "$input_program" ]; then
  echo "Error: The provided argument is not a valid file path."
  exit 1
fi

python3 main.py $input_program tmp.chr
swipl -q -l tmp.chr -g launcher -t halt | tr '\n' ';' | sed 's/;;/\n/g'
