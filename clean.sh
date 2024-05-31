#!/bin/bash

bench=( "nQueens/" ) #contains the directory to explore

benchDirectory="./benchmark/"


for b in $bench; do
    localPath="${benchDirectory}${b}"
    aspProgramDirectory="${localPath}ASP/"
    caspProgramDirectory="${localPath}CASP/"
    chrProgramDirectory="${localPath}CHR/"
    resultDir="${localPath}results/"
    
    #generate instances and then tests !
    cd $localPath
    echo "Cleaning the directory ./ASP"
    rm ./ASP/* #get rid of previous instances just to make sure everything is fine. 
    echo "Cleaning the directory ./CASP"
    rm ./CASP/*
    echo "Cleaning the directory ./CHR"
    rm ./CHR/*
    echo "Cleaning the directory ./results"
    rm ./results/*
    
    echo "Generating all instances..."
    python3 ./generateAllInstances.py #in each directory, there's a python script to generate instances. 
    echo "Generation done."
    echo ""
    
    cd ../../
    
    if [ -e "${localPath}resultsAll.txt" ]; then
        echo " -- Deleting the previous results obtained (All solution) -- "
        rm "${localPath}resultsAll.txt"
    fi
    if [ -e "${localPath}resultsFirst.txt" ]; then
        echo " -- Deleting the previous results obtained (First solution) -- "
        rm "${localPath}resultsFirst.txt"
    fi
    echo ""
    touch "${localPath}resultsAll.txt"
    touch "${localPath}resultsFirst.txt"
    echo "program name:compilation time (ASP):solving time (ASP):compilation time (CASP):solving time (CASP):compilation time (clingo):solving time (clingo)" >> "${localPath}resultsAll.txt"
    echo "program name:compilation time (ASP):solving time (ASP):compilation time (CASP):solving time (CASP):compilation time (clingo):solving time (clingo)" >> "${localPath}resultsFirst.txt"
done
