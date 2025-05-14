#!/bin/bash

# Check if exactly one argument is provided
if [ "$#" -ne 1 ]; then
  echo "Error: At least one argument is required. Try the option --help if you need more information on how to use this script."
  exit 1
fi

opts=() #Empty array of argument

while [[ $# -gt 0 ]]; do
  case "$1" in
    -v|--verbose)
      opts+=("-v")
      shift
      ;;
    -w|--well-founded)
      opts+=("-w")
      shift
      ;;
    -u|--unfounded)
      opts+=("-u")
      shift
      ;;
    -*)
      echo "Unknows option: $1" >&2
      exit 1
      ;;
  esac
done

input_program=$1
# Check if the argument is a valid path to a file
if [ ! -f "$input_program" ]; then
  echo "Error: The provided argument is not a valid file path."
  exit 1
fi

python3 main.py "${opts[@]}" $input_program tmp.chr
swipl -q -f scc.pl -l tmp.chr -g launcher -t halt | tr '\n' ';' | sed 's/;;/\n/g'
