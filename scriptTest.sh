#!/bin/bash

aspProgramDirectory="programASP"
chrProgramDirectory="programCHR"
resultDir="results"
testDir="expectedResults"

onHold=false

RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
NC='\033[0m' # No Color
BOLD=$(tput bold)
NORMAL=$(tput sgr0)

# test if the directory exists
if [ -d "$aspProgramDirectory" ]; then
    onHold=false
    cd "$aspProgramDirectory"

    # Names of the files
    files=()

    for file in *; do
        if [ -f "$file" ]; then
            files+=("${file%.asp}")
        fi
    done
    
    cd ..

    echo "Deleting previous results from ./"$resultDir"."
    rm ./$resultDir/*.txt
    
    echo "Number of test files found in te directory $aspProgramDirectory : ${#files[@]}"
    for file in "${files[@]}"; do
        echo -n "Treating file $aspProgramDirectory/$file.asp "
        python3 main.py $aspProgramDirectory/$file.asp ./$chrProgramDirectory/$file.chr
        if [ -f "./$chrProgramDirectory/$file.chr" ]; then
        
            time_before=$(date +%s%N)
            swipl -q -l "$chrProgramDirectory/$file.chr" -g launcher -t halt | tr '\n' ';' | sed 's/;;/\n/g' > ./$resultDir/$file.tmp
            time_after=$(date +%s%N)            elapsed_time=$(echo "scale=3; ($time_after - $time_before) / 1000000000" | bc | tr "." ",")
            solving_time=$(printf "%0.3f" "0$elapsed_time")
            exec 3< ./$resultDir/$file.tmp # open file in reading only
            # read line by line (each one is an answer set)
            numAnswerSet=0
            while read -r ligne <&3; do
                numAnswerSet=$(( $numAnswerSet+1 ))
                echo $ligne > ./$resultDir/$file\_$numAnswerSet.tmp
                cat ./$resultDir/$file\_$numAnswerSet.tmp | tr ';' '\n' | sort > ./$resultDir/$file\_$numAnswerSet.txt
                rm ./$resultDir/$file\_$numAnswerSet.tmp
            done
            exec 3<&- #close the file
            rm ./$resultDir/$file.tmp
            
            #Compare the expected with the real result
            isEqual=true
            for (( i=1 ; i <= numAnswerSet ; i++ )); do
                if [ ! -f "./$testDir/$file"\_"$numAnswerSet.txt" ]; then
                    echo -n -e "${ORANGE}${BOLD}ON HOLD.${NORMAL}${NC}"
                    onHold=true
                    isEqual=false
                    break
                else
                    hasAnAnswer=false
                    for (( j=1 ; j <= numAnswerSet ; j++ ))
                    do
                        if cmp -s "./$resultDir/$file"\_"$i.txt" "./$testDir/$file"\_"$j.txt"; then
                            hasAnAnswer=true
                            break
                        fi
                    done
                    if [ "$hasAnAnswer" = false ]; then
                        echo -n -e "${RED}${BOLD}FAIL.${NORMAL}${NC}"
                        isEqual=false
                        break
                    fi
                fi
            done
            if [ "$isEqual" = true ]; then
                echo -n -e "${GREEN}${BOLD}OK.${NORMAL}${NC}"
            fi
            echo " time: $solving_time s"
        else
            echo "The chr file hasn't been correctly generated..."
        fi
    done
    if $onHold ; then
        echo
        echo -e "${BOLD}- WARNING -${NORMAL}"
        echo "Some files are tagged 'on hold'. This means that there are no expected results for these files. You must confirm the results of these files by hand."
    fi
else
    echo "The directory $aspProgramDirectory doesn't exists."
fi
