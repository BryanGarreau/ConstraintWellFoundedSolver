# CASP solver

This project is a CASP solver based on a simple translation from CASP to CHR. Our solver gives the Constraint Well-Founded Model as it is defined in our article. This solver is strongly inspired by the translation from ASP to CHR made by Stephan. 

## Swi-Prolog powered solver

The program is in the first place translated to an equivalent CHR-prolog program that is then solved by a prolog solver (SWI-Prolog in our case). This program was executed and tested on SWI-Prolog version 8.2.4 for x86_64-linux and Python version 3.9.2. 

## Directory description

The directory expectedResults contains all the expected results from the example program in programASP for testing purposes. If the one of the program is modified, the results from earlier experiments should stay the same. 
The directory results contains all the results of the programs obtained by the testing script.
The directory constraints contains all the CHR rules that are needed to solve constraints. Each file contains the chr rules to declare and solve a special type of constraint. They cannot be used alone, they all need to be put in a program to be used correctly. 

## script

The python files contain the parser that translates CASP to CHR programs and can be used directly calling them in Python or via our bash scripts. 

The script scriptTest.sh reads all the files in programASP to translates and solve them and compare the results to expected results for development purposes.

## How to use

The script solve.sh takes an ASP file in input and returns all the CWFM obtained. You can execute the script directly in a console like this:

``` ./solve.sh ASPfileName ```

for example, you can solve the program presented in our paper like this:

``` ./solve.sh ./programASP/ICLP_exCLP1.asp ```

and 

``` ./solve.sh ./programASP/ICLP_exASP.asp ```

### How to use the translator

You can use the translator in different ways. First you can call the python script via python:

``` python main.py ASPfileName CHRfileName ```

Where ASPfileName corespond to the file that you want to translate and CHRfileName the name of the file that will be created. You can also specify the path to each file. The name of the file also contains the path to the file you indicate. 

### How to use swipl with our CHR files

To solve the chr you can use :

``` swipl -l CHRfileName -g launcher -t halt ```


