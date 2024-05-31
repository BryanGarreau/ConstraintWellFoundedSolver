import copy as copy
from structure import *


class WellFoundedModel:
    def __init__(self,prog,constraint=[],verbose=False):
        self.prog = prog
        self.constraint = constraint
        self._I = set()
        self._J = set()

        for r in self.prog:
            self._J.add(r.head.atom) #We head all possible atoms to J

        self.verbose = verbose

        if verbose:
            print("Well Founded set.")
            print("Here's the partial interpretation")
            self.show()

    def phiOperator(self,I,J,P):
        #I represent atoms that are certain
        #J represent atoms that are possible
        #P represent the program
        ca = set() #consequence atoms

        for r in P: #For every rule
            satisfiable = True #True if the body is satisfiable. 

            if self.verbose:
                print()
                print("Processing rule ", r )
            for i in r.body:
                if self.verbose:
                    print("    processing the atom ", i, " of sign", i.sign)
                    print(not i.atom in I)
                    print(i.atom in J)
                if ((i.sign == True) and (not i.atom in I)):
                    satisfiable = False
                    if self.verbose:
                        print("        ", i.atom," is not in I")
                    break
                if ((i.sign == False) and (i.atom in J)):
                    satisfiable = False
                    if self.verbose:
                        print("        ", i.atom," is in J")
                    break
            if satisfiable:
                if self.verbose:
                    print("        Adding rule ", r)
                ca.add(copy.deepcopy(r.head.atom))
        return ca

    def consequence(self):
        newI = self.phiOperator(self._I, self._J, self.prog)
        newJ = self.phiOperator(self._J, self._I, self.prog)

        if(self.verbose):
            print("Consequence : ")
            print("I : ")
            for i in newI:
                print(i,end=", ")
            print()
            print("J : ")
            for i in newJ:
                print(i,end=", ")
            print()

        return newI, newJ

    def unfoundedSet(self):
        uset = set()

        fixpoint = False

        while not fixpoint:
            fixpoint = True
            for r in self.prog:
                for b in r.body:
                    if not b.sign and b.atom in self._I:
                        uset.add(r.head)
                        fixpoint = False
                    elif b.sign and not b.atom in self._J:
                        uset.add(r.head)
                        fixpoint = False
                    elif b.atom in uset:
                        uset.add(r.head)
                        fixpoint = False
        return uset
        

    def fixpoint(self):
        fxpnt = False #Have we found a fixpoint yet ? 
        while(not fxpnt):
            newI, newJ = self.consequence()
            # newPI = PartialInterpretation(newI,newJ)
            if self._I == newI and self._J == newJ :
                fxpnt = True
            else :
                self._I = copy.deepcopy(newI)
                self._J = copy.deepcopy(newJ)
        if self.verbose:
            print("Found a fixpoint")

    def show(self):
        print("I : ")
        for i in self._I:
            print(i,end=", ")
        print()
        print("J : ")
        for i in self._J:
            print(i,end=", ")
        print()

    def is_solution(self):
        if self._I == self._J: #equilibrium condition
            for i in self.constraint: #Checking for violated constraint
                violated = True
                for atom in i:
                    if not atom in self._I:
                        violated = False
                        break
                if violated:
                    return False
            return True #No constraint is violated
        return False

    def delete(self, at):
        if at in self._J:
            self._J.remove(at)
    
    def add(self, at):
        self._I.add(at)
        