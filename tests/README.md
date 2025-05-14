# Tests Directory

This directory contains all the files needed to tests our solver. The tests are separated in three categories: complete solving, constraint well-founded and unfouded sets.

As the name imply, the first category tests if the complete solving works as intended (ie. the solutions of the programs are correct), the second category tests if the well-founded model is correct and finally the last one shows the computed unfouded-sets to be sure that they are correct.


If the solver works as intended, all the tests should be "OK". In case you want to modify the solver, you can test your modification to see if the solver still works as intended.

The tests programs in the directory `programASP` is full of example programs.

To start the tests, you simply need to execute the script `./testScript.sh`

The script will translate CASP programs from the directory `programASP` in CHR (swi-prolog) in the directory `programCHR` and then store the results in the directory `results`
