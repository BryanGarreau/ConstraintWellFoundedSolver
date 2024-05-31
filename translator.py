import os
from structure import *

def appendSymbolsTable(s,r,x,n): #symbols, rules, symbol, rule's number
    for i in range(len(s)):
        if x == s[i]:
            r[i].append(n)
            return 
    s.append(x)
    r.append([n])
        
def appendSymbol(s,r,x): #symbols, rules, symbol, rule's number
    for i in range(len(s)):
        if x == s[i]:
            return 
    s.append(x)
    r.append([])

def translate(prog,facts,constraintFacts,solveChoicePoint = False, nbSol=0, cleanOutput = True):

    #solveChoicePoint false == well founded semantics
    #solveChoicePoint true == finding solution to the program
    
    #nbSol == 0 means all the solutions
    #nbSol == 1 means return the first solution
    
    #cleanOutput == true cleans the ouput of the program from useless predicate
    #cleanoutput == false keeps useless atoms for debugging purposes. 
    
    constrainedProgram = True #True if there is constraint in the program.
    #useless for now. might be useful to make a faster program when there is no constraints. 
    
    symbols = [] #contains all the propositional atoms of the program
    rules = [] #contains the list of rules where the symbols appear
    # symbols = [a] and rules = [[1,2,3]] means that a appears in the rules 1,2,3.
    
    factSet = set()
    
    for i in facts:
        factSet.add(i.__str__())
    
    
    # Header
    header = ":- use_module(library(chr)).\n:- chr_constraint fact/1, rule/4, nrule/1, nhead/1, head/2, heads/2, bodyP/2, bodyN/2, bodyC/2, launcher/0, end/0, cleaner/0, choice/1, choi_nrule/3, choi_frule/1, verified_constraint/2, unsat_constraint/2, bot/0.\n\n"
    # Program
    exampleProg = "%%Program\n\n"
    # Head of the rules
    headOfRules = "%% Head of the rules \n\nfact(bot) <=> fail.\nnrule(X) \ head(X,Y), heads(Y,C) <=> A is C-1 | heads(Y,A).\nheads(bot,_) <=> true.\nheads(X,0) <=> nhead(X).\nnhead(bot) <=> true.\n"
    # Transformation
    transformation = "%% Transformation \n\nred_neg @ fact(X) \ bodyN(Y,X), rule(Y,_,_,_) <=> nrule(Y).\nred_fai @ nhead(X) \ bodyP(Y,X), rule(Y,_,_,_) <=> nrule(Y).\nred_pos @ nhead(X) \ bodyN(Y,X), rule(Y,P,N,C) <=> A is N-1 | rule(Y,P,A,C).\nred_suc @ fact(X) \ bodyP(Y,X), rule(Y,P,N,C) <=> A is P-1 | rule(Y,A,N,C).\n\nred_con_success @ verified_constraint(X,Y) \ bodyC(X,Y), rule(X,P,N,C) <=> A is C-1 | rule(X,P,N,A).\nred_con_failure @ unsat_constraint(X,Y) \ bodyC(X,Y), rule(X,_,_,_) <=> nrule(X).\n\n"
    # Constraint propagation
    constraintPropagation = "%% Constraint propagation\n\n"
    # Empty body
    emptyBody ="%% Empty body \n\nhead(X,Y), rule(X,0,0,0) <=> fact(Y).\n\n"
    # Choice phase
    #choiceRules ="%% Choice\n\n%% The rule is forced to be true.\n%% The negative body cannot be true\nchoi_frule(X), bodyN(X,Y), fact(Y) <=> fail.\n\n%% The rule is forced to be false\n%% If one atom from the negative body is true, then fail.\nnhead(Y) \ choi_nrule(X,Z), bodyN(X,Y) <=> choi_nrule(X,A), A is Z-1.\nchoi_nrule(_,0) <=> fail.\n\nrule(X,0,Z,_), choice(X) <=> (choi_frule(X), rule(X,0,0,0) ; choi_nrule(X,Z), nrule(X)).\n\n"
    
    choiceRules ="%% Choice\n\n%% The rule is forced to be true.\n%% The negative body cannot be true\nchoi_frule(X), bodyN(X,Y), fact(Y) <=> fail.\nchoi_frule(X) \ bodyC(X,Y) <=> fact(Y).\n\n%% The rule is forced to be false\n%% If one atom from the negative body is true, then fail.\nnhead(Y) \ choi_nrule(X,Z,C), bodyN(X,Y) <=> A is Z-1 | choi_nrule(X,A,C).\n\nchoi_nrule(X,Z,C), verified_constraint(X,_) <=> A is C-1 | choi_nrule(X,Z,A).\nchoi_nrule(_,0,0) <=> fail.\n\n%%rule(X,0,Z,C), choice(X) <=> (choi_frule(X), rule(X,0,0,0) ; choi_nrule(X,Z,C), nrule(X)).\nenumeration @ dom(X,[V|Rest]) <=> length(Rest,Length), Length =\= 0 | dom(X,[V]) ; dom(X,Rest).\n\n"
    
    # Printing solutions and fail
    if nbSol == 0:
        printSol = "end <=> chr_show_store(user), nl, fail.\n"
    elif nbSol == 1:
        printSol = "end <=> chr_show_store(user), nl.\n"
    else:
        print("ERROR. Cannot translate program for a number of solutions different from 0 or 1. (For now at least... Might be fixed in next version).")
        exit(1)
        
    # Cleaner
    cleaner = "%% Cleaner \n\nfact(X) \ fact(X) <=> true.\ncleaner \ bodyP(_,_) <=> true.\ncleaner \ bodyN(_,_) <=> true.\ncleaner \ head(_,_) <=> true.\ncleaner \ bodyC(_,_) <=> true.\ncleaner \ choice(_) <=> true.\ncleaner \ choi_frule(_) <=> true.\ncleaner \ choi_nrule(_,_,_) <=> true.\n%%cleaner \ nhead(_) <=> true.\ncleaner \ nrule(_) <=> true.\ncleaner \ rule(_,_,_,_) <=> true.\ncleaner \ heads(_,_) <=> true.\ncleaner <=> true.\n\n"
    # Launcher
    launcher = "%% Launcher \n\n"
    emptyLauncher = True

    # Adding all the constraint solver to the constraint propagation part
    c_list = [] #contains all the constraints added
    for fileName in os.listdir("./constraints/"):
        filePath = os.path.join("./constraints/", fileName)
        if os.path.isfile(filePath) and fileName[-4:] == ".chr" :
            with open(filePath, 'r') as f:
                for line in f:
                    if line[0] == "#":
                        c_list.append(line[1:-1]) #The line starting with # contains the declaration
                    else:
                        constraintPropagation += line
                constraintPropagation += "\n"
    
    # Constraint declaration with arity
    constraintDeclaration = "%% Constraint declaration\n\n"
    if len(c_list) > 0:
        constraintDeclaration += ":- chr_constraint "
        
    for i in range(0,len(c_list)-1):
        constraintDeclaration += c_list[i] + ", "
    if len(c_list) > 0:
        constraintDeclaration += c_list[-1] + ".\n\n"
    
    ruleNumber = 1

    launcher += "launcher <=> "
       
    #let's add facts to the launcher
    launcher += ', '.join(str("fact("+f.__str__()+")") for f in facts)
    
    #let's add domains and facts constraints to the launcher
    launcher += ', '.join(str(c) for c in constraintFacts)
    if len(facts) + len(constraintFacts) > 0:
        emptyLauncher = False
        if len(prog) > 0:
            launcher += ", "

    
    #let's iterate on each rule except the last one.
    for i in range(len(prog)-1): 
        numNeg = 0
        numPos = 0
        numCon = len(prog[i].constraints)
        
        for b in prog[i].body:
            if b.sign:
                numPos = numPos + 1
            else:
                numNeg = numNeg + 1 
        launcher += "rule(" + str(ruleNumber) + "," + str(numPos) + "," + str(numNeg) + "," + str(numCon) + "), head("+ str(ruleNumber) + "," + prog[i].head.__str__() + ")"
        emptyLauncher = False
        
        if len(prog[i].body) > 0: #if there's no body, do nothing. (empty else)
            launcher += ", "
            #adding positive and negative body to the launcher
            for j in range(len(prog[i].body)-1):
                appendSymbol(symbols,rules,prog[i].body[j].atom)
                if prog[i].body[j].sign:
                    launcher += "bodyP(" + str(ruleNumber) + "," + prog[i].body[j].atom.__str__() + ")" + ', '
                else:
                    launcher += "bodyN(" + str(ruleNumber) + "," + prog[i].body[j].atom.__str__() + ")" + ', '
            if prog[i].body[-1].sign:
                launcher += "bodyP(" + str(ruleNumber) + "," + prog[i].body[-1].atom.__str__() + ")" + ', '
            else:
                launcher += "bodyN(" + str(ruleNumber) + "," + prog[i].body[-1].atom.__str__() + ")" + ', '
            appendSymbol(symbols,rules,prog[i].body[-1].atom)
        else:
            pass #empty body
        #adding constraints to the launcher
        if len(prog[i].constraints) > 0:
            if len(prog[i].body) < 1:
                launcher += ", "
            for j in range(len(prog[i].constraints)-1):
                launcher += "bodyC(" + str(ruleNumber) + "," + prog[i].constraints[j].name + ")" + ', '
            launcher += "bodyC(" + str(ruleNumber) + "," + prog[i].constraints[-1].name + ")" + ', '

            
        #emptyBody += "rule(" + str(ruleNumber) + ",0) <=> fact(" + prog[i].head.__str__() + ").\n"
        exampleProg += "%% @r" + str(ruleNumber) + "  " + prog[i].__str__()  + "\n"
        if not isinstance(prog[i].head,Constraint):
            appendSymbolsTable(symbols,rules,prog[i].head.atom,ruleNumber)
        ruleNumber += 1
    
    #last iteration on the rules
    if len(prog) > 0: # If there's no rule, then there's nothing to add. 
        numNeg = 0
        numPos = 0
        numCon = len(prog[-1].constraints)
        for b in prog[-1].body:
            if b.sign:
                numPos = numPos + 1
            else:
                numNeg = numNeg + 1
        launcher += "rule(" + str(ruleNumber) + "," + str(numPos) + "," + str(numNeg) + "," + str(numCon) + "), head("+ str(ruleNumber) + "," + prog[-1].head.__str__() + ")"
        emptyLauncher = False
        
        if len(prog[-1].body) > 0:
            launcher += ", "
        for j in range(len(prog[-1].body)-1):
            appendSymbol(symbols,rules,prog[-1].body[j].atom)
            if prog[-1].body[j].sign:
                launcher += "bodyP(" + str(ruleNumber) + "," + prog[-1].body[j].atom.__str__() + ")" + ', '
            else:
                launcher += "bodyN(" + str(ruleNumber) + "," + prog[-1].body[j].atom.__str__() + ")" + ', '
        if len(prog[-1].body) > 0:
            if prog[-1].body[-1].sign:
                launcher += "bodyP(" + str(ruleNumber) + "," + prog[-1].body[-1].atom.__str__() + ")"
            else:
                launcher += "bodyN(" + str(ruleNumber) + "," + prog[-1].body[-1].atom.__str__() + ")"
            appendSymbol(symbols,rules,prog[-1].body[-1].atom)
        
        if len(prog[-1].constraints) > 0:
            launcher += ', '
            for j in range(len(prog[-1].constraints)-1):
                launcher += "bodyC(" + str(ruleNumber) + "," + prog[-1].constraints[j].name + ")" + ', '
            launcher += "bodyC(" + str(ruleNumber) + "," + prog[-1].constraints[-1].name + ")"
        
        exampleProg += "%% @r" + str(ruleNumber) + "  " + prog[-1].__str__()  + "\n"
        if not isinstance(prog[-1].head,Constraint):
            appendSymbolsTable(symbols,rules,prog[-1].head.atom,ruleNumber)
        
        ruleNumber += 1
 
    # symbols = [a] and rules = [[1,2,3]] means that a appears in the rules 1,2,3
    for i in range(len(symbols)):
        if rules[i] != []:
            launcher += ", heads(" + symbols[i].__str__() + "," + str(len(rules[i])) + ")"
        elif not emptyLauncher:
            if not symbols[i].__str__() in factSet:
                launcher += ", nhead(" + symbols[i].__str__() + ")"
        else:
            if not symbols[i].__str__() in factSet:
                emptyLauncher = False
                launcher += "nhead(" + symbols[i].__str__() + ")"

    #if solveChoicePoint:
        #for i in range(1,ruleNumber):
            #if not prog[i-1].isIntegrityConstraint():
                #launcher += ", choice(" + str(i) + ")"
    
    if cleanOutput:
        launcher += ", cleaner"
    launcher += ", end.\n"
    headOfRules += "\n"
    #print(header)
    #print(exampleProg)
    #print(headOfRules)
    #print(transformation)
    #print(emptyBody)
    #print(cleaner)
    #print(launcher)
    
    #return header + exampleProg + headOfRules + transformation + emptyBody + choiceRules + launcher + cleaner + printSol
    return header + exampleProg + headOfRules + constraintDeclaration + constraintPropagation + transformation + emptyBody + choiceRules + launcher + cleaner + printSol
