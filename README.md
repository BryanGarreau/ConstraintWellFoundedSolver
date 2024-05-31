# CASP solver

This project is a CASP solver based on a simple translation from CASP to CHR. This solver is strongly inspired by the translation from ASP to CHR made by Stephan [cite]

## Swi-Prolog powered solver

The program is in the first place translated to an equivalent CHR-prolog program that is then solved by a prolog solver (Swiprolog in our case). This process 

## Directory description

The directory expectedResults contains all the results from the example program in programASP.
The directory results contains all the real results of the programs.
The directory constraints contains all the chr propagators that are needed to solve constraints. Each file contains the chr rules to declare and solve a special type of constraint. They cannot be used alone, they all need to be put in a program to be used correctly. 

## script

The python files contain the parser that translates CASP to CHR programs.

the script scriptTest.sh reads all the files i programASP to translates and solve them and compare the results to results.

## How to use

You can use the translator in different ways. First you can call the python script via python :

``` python main.py ASPfileName CHRfileName ```

Where ASPfileName corespond to the file that you want to translate and CHRfileName the name of the file that will be created. You can also specify the path to each file.

To solve the chr you can use :

``` swipl -l fileName -g launcher -t halt ```
