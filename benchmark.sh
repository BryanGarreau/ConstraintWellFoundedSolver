#!/bin/bash

bench=( "nQueens/" ) #contains the directory to explore

benchDirectory="./benchmark/"


for b in $bench; do
    localPath="${benchDirectory}${b}"
    aspProgramDirectory="${localPath}ASP/"
    caspProgramDirectory="${localPath}CASP/"
    chrProgramDirectory="${localPath}CHR/"
    resultDir="${localPath}results/"
    
    cd "./${localPath}/ASP/"
    # Names of the files
    files=()
    for file in *; do
        if [ -f "$file" ]; then
            files+=("${file%.asp}")
        fi
    done
    cd ../../../
    
    for file in "${files[@]}"; do
        
        resultLineFirst="${file}:"
        resultLineAll="${file}:"
        
        ##________ TREATING ASP FILE ALL ________##
        
        echo "Treating $file :"
        echo -e "\t(All solution)"
        
        compilationTime=$( { time -p python3 main.py "${aspProgramDirectory}${file}.asp" "${chrProgramDirectory}${file}0.chr" -n 0 ;} 2>&1 | grep user | awk '{print $2}' )
        
        echo -e "\t\tcompilation time : $compilationTime"
        resultLineAll+="${compilationTime}:"
        
        solving_time=$( { time -p swipl -q -l "${chrProgramDirectory}${file}0.chr" -g launcher -t halt | tr '\n' ';' | sed 's/;;/\n/g' > "${resultDir}${file}0.tmp" ;} 2>&1 | grep user | awk '{print $2}' )
        
        echo -e "\t\ttotal solving time : $solving_time"
        resultLineAll+="${solving_time}:"
        
        ##________ TREATING ASP FILE FIRST ________##
        
        echo -e "\t(First solution)"
        
        compilationTime=$( { time -p python3 main.py "${aspProgramDirectory}${file}.asp" "${chrProgramDirectory}${file}1.chr" -n 1 ;} 2>&1 | grep user | awk '{print $2}' )
        
        echo -e "\t\tcompilation time : $compilationTime"
        #echo -n "${compilationTime}:" >> "${localPath}resultsFirst.txt"
        
        solving_time=$( { time -p  swipl -q -l "${chrProgramDirectory}${file}1.chr" -g launcher -t halt | tr '\n' ';' | sed 's/;;/\n/g' > "${resultDir}${file}1.tmp" ;} 2>&1 | grep user | awk '{print $2}' )
        
        echo -e "\t\ttotal solving time : $solving_time"
        resultLineFirst+="${solving_time}:"
        
        ##________ TREATING CASP FILE ALL ________##
        
        echo "Treating ${file}.casp :"
        echo -e "\t(All solution)"
        
        compilationTime=$( { time -p python3 main.py "${caspProgramDirectory}${file}.casp" "${chrProgramDirectory}${file}CASP0.chr" -n 0 ;} 2>&1 | grep user | awk '{print $2}' )
        
        echo -e "\t\tcompilation time : $compilationTime"
        #echo -n "${compilationTime}:" >> "${localPath}resultsAll.txt"
        resultLineAll+="${compilationTime}:"
        
        solving_time=$( { time -p swipl -q -l "${chrProgramDirectory}${file}CASP0.chr" -g launcher -t halt | tr '\n' ';' | sed 's/;;/\n/g' > "${resultDir}${file}CASP0.tmp" ;} 2>&1 | grep user | awk '{print $2}' )

        echo -e "\t\ttotal solving time : $solving_time"
        resultLineAll+="${solving_time}:"
        
        ##________ TREATING CASP FILE FIRST ________##
        
        echo -e "\t(First solution)"

        compilationTime=$( { time -p python3 main.py "${caspProgramDirectory}${file}.casp" "${chrProgramDirectory}${file}CASP1.chr" -n 1 ;} 2>&1 | grep user | awk '{print $2}' )

        echo -e "\t\tcompilation time : $compilationTime"
        echo -n "${compilationTime}:" >> "${localPath}resultsFirst.txt"
        
        solving_time=$( { time -p swipl -q -l "${chrProgramDirectory}${file}CASP1.chr" -g launcher -t halt | tr '\n' ';' | sed 's/;;/\n/g' > "${resultDir}${file}CASP1.tmp" ;} 2>&1 | grep user | awk '{print $2}' )
        
        echo -e "\t\ttotal solving time : $solving_time"
        resultLineFirst+="${solving_time}:"
        
        ##________ CLINGO SOLVING ALL ________##
        
        echo "Treating ${file}.asp with clingo :"
        echo -e "\t(All solution)"
        
        echo -e "\t\tcompilation time : ?????"
        resultLineAll+=":"
        
        solving_time=$( { time -p clingo -q -n 0 "${aspProgramDirectory}${file}.asp" 1> /dev/null ;} 2>&1 | grep user | awk '{print $2}' )

        echo -e "\t\ttotal solving time : $solving_time"
        resultLineAll+="${solving_time}"

        ##________ CLINGO SOLVING FIRST ________##

        echo -e "\t(First solution)"
        
        echo -e "\t\tcompilation time : ?????"
        resultLineFirst+=":"
        
        solving_time=$( { time -p clingo -q -n 1 "${aspProgramDirectory}${file}.asp" 1> /dev/null ;} 2>&1 | grep user | awk '{print $2}' )

        echo -e "\t\ttotal solving time : $solving_time"
        resultLineFirst+="${solving_time}"
        echo ""
        
        
        echo "${resultLineFirst}" >> "${localPath}resultsFirst.txt"
        echo "${resultLineAll}" >> "${localPath}resultsAll.txt"
    done
done
