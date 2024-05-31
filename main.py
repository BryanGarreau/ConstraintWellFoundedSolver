import sys
from parser import  *
from structure import *
from translator import *

verbose = False
solveChoice = False
nbSol = 0 #default value = all


if len(sys.argv) == 2 or len(sys.argv) > 6:
    if sys.argv[1] != "--help":
        print("Too many arguments !")
    print("How to correctly call this program :")
    print("\t python3 main.py inputFileName outputFileName --options")
    print("options :")
    print("\t -v : enable verbose (disabled by default)")
    print("\t -s : enable solving (only well-founded model by default)")
    print("\t -d : debug option. Disables the clean output of the CHR program")
    print("\t -n : number of solutions desired (0 meaning all solutions)")
    print("\t --help : help.")
    exit()
    
asp_program = ""
if verbose:
 print("Open file...")
 
#if len(sys.argv) > 1 :
    #inputFileName = sys.argv[1]
    #outputFileName = sys.argv[2]
    #fileInput = open(inputFileName,"r")
    #lines = fileInput.readlines()
    #asp_program = ""
    #for l in lines:
        #asp_program += l
    #fileOutput = open(outputFileName,"w")
if len(sys.argv) > 1 :
    inputFileName = sys.argv[1]
    outputFileName = sys.argv[2]
    fileInput = open(inputFileName,"r")
    lines = fileInput.readlines()
    asp_program = ""
    for l in lines:
        asp_program += l
    fileOutput = open(outputFileName,"w")
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "-v":
            verbose = True
        elif sys.argv[i] == "-s":
            solveChoice = True
        elif sys.argv[i] == "-d":
            cleanOutput = False #for debug
        elif sys.argv[i] == "-n":
            i += 1
            nbSol = int(sys.argv[i])
        else :
            print("unrecognised argument")
            print(sys.argv[i])
            exit(1)
        i += 1
if verbose:
 print("Parsing...")

r, facts, constraints = parse_asp(asp_program,False)#Rules, facts, constraints


#program TEST
#r = []
#r.append(Rule( Literal(Atom('a')), #positiv
              #[Literal(Atom('b',True))], #negativ
              #[Constraint('leq3(x,3,y)')])) #constraint

#facts = []
#constraints = []
#constraints.append(Constraint('dom(x,[1,2])'))
#constraints.append(Constraint('dom(y,[4,5])'))



#r, facts, c = parse_asp(asp_program,verbose)#Rules, facts, constraints
prog = r #r contains all the rules of the program.

if verbose:
 print("Program parsed.")

resultingProg = translate(prog,facts,constraints,True,nbSol)
fileOutput.write(resultingProg)

fileInput.close()
fileOutput.close()



