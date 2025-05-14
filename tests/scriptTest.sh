#!/bin/bash

translatorDirectory="../"
aspProgramDirectory="programASP"
chrProgramDirectory="programCHR"
resultDirSolving="results/complete_solving"
resultDirWellFounded="results/well_founded"
resultDirUnfounded="results/unfounded"
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
    if [ -d "./$resultDirSolving/" ]; then
        rm ./$resultDirSolving/*.txt
    else
        mkdir ./$resultDirSolving
        echo "Creating the directories for complete solving tests."
    fi
    if [ -d "./$resultDirWellFounded/" ]; then
        rm ./$resultDirWellFounded/*.txt
    else
        mkdir ./$resultDirWellFounded
        echo "Creating the directories for well-founded tests."
    fi
    if [ -d "./$resultDirUnfounded/" ]; then
        rm ./$resultDirUnfounded/*.txt
    else
        mkdir ./$resultDirUnfounded
        echo "Creating the directories for unfounded tests."
    fi
    
    echo "Number of test files found in te directory $aspProgramDirectory : ${#files[@]}"
    echo -e "Warning : Each test has a ${BOLD}30s${NORMAL} timeout for compilation and ${BOLD}30s${NORMAL} for execution."

#TEST SOLVING
    echo -e "\nTests for full solving.\n"
    for file in "${files[@]}"; do
        echo -n "Treating file $aspProgramDirectory/$file.asp "
        timeout 30s python3 "${translatorDirectory}/main.py" $aspProgramDirectory/$file.asp ./$chrProgramDirectory/$file\_solving.chr -s
        if [ -f ./$chrProgramDirectory/$file\_solving.chr ]; then
        
            time_before=$(date +%s%N)
            #timeout 30s swipl -q -f "../scc.pl" -l ./$chrProgramDirectory/$file\_solving.chr -g launcher -t halt | tr '\n' ';' | sed 's/;;/\n/g' > ./$resultDirSolving/$file\_solving.tmp
            #timeout 30s swipl -q -f "../scc.pl" -l ./$chrProgramDirectory/$file\_solving.chr -g launcher -t halt | tr '\n' ';' | sed 's/;;//g' | sed 's/\./\n/g' > ./$resultDirSolving/$file\_solving.tmp
            timeout 30s swipl -q -f "../scc.pl" -l ./$chrProgramDirectory/$file\_solving.chr -g launcher -t halt | awk '{if ($0 == ".") {print answer;answer = "";} else {answer = (answer == "" ? $0 : answer " " $0);}} END {if (answer != "") print answer;}' | tr ' ' ';' > ./$resultDirSolving/$file\_solving.tmp
            time_after=$(date +%s%N)
            elapsed_time=$(echo "scale=3; ($time_after - $time_before) / 1000000000" | bc | tr "." ",")
            solving_time=$(printf "%0.3f" "0$elapsed_time")
            exec 3< ./$resultDirSolving/$file\_solving.tmp # open file in reading only
            # read line by line (each one is an answer set)
            numAnswerSet=0
            while read -r ligne <&3; do
                numAnswerSet=$(( $numAnswerSet+1 ))
                echo $ligne > ./$resultDirSolving/$file\_solving\_$numAnswerSet.tmp
                cat ./$resultDirSolving/$file\_solving\_$numAnswerSet.tmp | tr ';' '\n' | sort > ./$resultDirSolving/$file\_solving\_$numAnswerSet.txt
                rm ./$resultDirSolving/$file\_solving\_$numAnswerSet.tmp
            done
            exec 3<&- #close the file
            rm ./$resultDirSolving/$file\_solving.tmp
            
            #Compare the expected with the real result
            isEqual=true
            if [ $numAnswerSet -eq 0 ]; then
                isEqual=false
                echo -n -e "${RED}${BOLD}FAIL.${NORMAL}${NC} No solution for this program."
            else
                for (( i=1 ; i <= numAnswerSet ; i++ )); do
                    if [ ! -f ./$testDir/complete_solving/$file\_solving\_$numAnswerSet.txt ]; then
                        echo -n -e "${ORANGE}${BOLD}ON HOLD.${NORMAL}${NC}"
                        onHold=true
                        isEqual=false
                        break
                    else
                        hasAnAnswer=false
                        for (( j=1 ; j <= numAnswerSet ; j++ ))
                        do
                            if cmp -s ./$resultDirSolving/$file\_solving\_$i.txt ./$testDir/complete\_solving/$file\_solving\_$j.txt ; then
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
            fi
            if [ "$isEqual" = true ]; then
                echo -n -e "${GREEN}${BOLD}OK.${NORMAL}${NC}"
            fi
            echo " time: $solving_time s"
        else
            echo "The chr file hasn't been correctly generated..."
        fi
    done

#TEST WELL FOUNDED
    echo -e "\nTests for well founded.\n"
    for file in "${files[@]}"; do
        echo -n "Treating file $aspProgramDirectory/$file.asp "
        timeout 30s python3 "${translatorDirectory}/main.py" $aspProgramDirectory/$file.asp ./$chrProgramDirectory/$file\_well\_founded.chr
        if [ -f ./$chrProgramDirectory/$file\_well\_founded.chr ]; then

            time_before=$(date +%s%N)
            #timeout 30s swipl -q -f "../scc.pl" -l ./$chrProgramDirectory/$file\_well\_founded.chr -g launcher -t halt | tr '\n' ';' | sed 's/;;//g' | sed 's/./\n/g' > ./$resultDirWellFounded/$file\_well\_founded.tmp
            timeout 30s swipl -q -f "../scc.pl" -l ./$chrProgramDirectory/$file\_well\_founded.chr -g launcher -t halt | awk '{if ($0 == ".") {print answer;answer = "";} else {answer = (answer == "" ? $0 : answer " " $0);}} END {if (answer != "") print answer;}' | tr ' ' ';' > ./$resultDirWellFounded/$file\_well\_founded.tmp
            time_after=$(date +%s%N)
            elapsed_time=$(echo "scale=3; ($time_after - $time_before) / 1000000000" | bc | tr "." ",")
            solving_time=$(printf "%0.3f" "0$elapsed_time")
            exec 3< ./$resultDirWellFounded/$file\_well\_founded.tmp # open file in reading only
            # read line by line (each one is an answer set)
            numAnswerSet=0
            while read -r ligne <&3; do
                numAnswerSet=$(( $numAnswerSet+1 ))
                echo $ligne > ./$resultDirWellFounded/$file\_well\_founded\_$numAnswerSet.tmp
                cat ./$resultDirWellFounded/$file\_well\_founded\_$numAnswerSet.tmp | tr ';' '\n' | sort > ./$resultDirWellFounded/$file\_well\_founded\_$numAnswerSet.txt
                rm ./$resultDirWellFounded/$file\_well\_founded\_$numAnswerSet.tmp
            done
            exec 3<&- #close the file
            rm ./$resultDirWellFounded/$file\_well\_founded.tmp

            #Compare the expected with the real result
            isEqual=true
            if [ $numAnswerSet -eq 0 ]; then
                isEqual=false
                echo -n -e "${RED}${BOLD}FAIL.${NORMAL}${NC} No solution for this program."
            else
                for (( i=1 ; i <= numAnswerSet ; i++ )); do
                    if [ ! -f ./$testDir/well\_founded/$file\_well\_founded\_$numAnswerSet.txt ]; then
                        echo -n -e "${ORANGE}${BOLD}ON HOLD.${NORMAL}${NC}"
                        onHold=true
                        isEqual=false
                        break
                    else
                        hasAnAnswer=false
                        for (( j=1 ; j <= numAnswerSet ; j++ ))
                        do
                            if cmp -s ./$resultDirWellFoundeds/$file\_well\_founded\_$i.txt ./$testDir/\_well\_founded/$file\_well\_founded\_$j.txt ; then
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
            fi
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
