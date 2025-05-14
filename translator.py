import os
from structure import *
dir_path = os.path.dirname(os.path.realpath(__file__))

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

def isConstraint(atom):
    return isinstance(atom,Constraint)

def translate(prog, facts, constraintFacts, solveChoicePoint = False, nbSol=0, cleanOutput = True, showSCC = False):

    #showSCC false == the program returns the "clean" solution
    #showSCC true == showing scc for debugging purposes and for testing purposes

    #solveChoicePoint false == well founded semantics
    #solveChoicePoint true == finding solution to the program
    
    #nbSol == 0 means all the solutions
    #nbSol == 1 means return the first solution
    
    #cleanOutput == true cleans the ouput of the program from useless predicate
    #cleanoutput == false keeps useless atoms for debugging purposes. 
    
    #constrainedProgram = True #True if there is constraint in the program.#Not used anymore. Uncomment if needed.
    #useless for now. might be useful to make a faster program when there is no constraints. 
    
    symbols = [] #contains all the propositional atoms of the program
    rules = [] #contains the list of rules where the symbols appear
    # symbols = [a] and rules = [[1,2,3]] means that a appears in the rules 1,2,3.
    
    factSet = set()
    
    for i in facts:
        factSet.add(i.__str__())
    
    
    # Header
    header = ":- use_module(library(chr)).\n[scc].\n:- chr_constraint fact/1, rule/4, nrule/1, nhead/1, head/2, heads/2, bodyP/2, bodyN/2, bodyC/2, launcher/0, end/0, cleaner/0, choice/1, choi_nrule/3, choi_frule/1, verified_constraint/2, unsat_constraint/2, bot/0.\n\n"
    arcArray=[]
    # Program
    exampleProg = "%%Program\n\n"
    # Head of the rules
    headOfRules = "%% Head of the rules \n\nfact(bot) <=> fail.\nnrule(X) \ head(X,Y), heads(Y,C) <=> A is C-1 | heads(Y,A).\nheads(bot,_) <=> true.\nheads(X,0) <=> nhead(X).\nnhead(bot) <=> true.\n"
    # Transformation
    transformation = "%% Transformation \n\nred_neg @ fact(X) \ bodyN(Y,X), rule(Y,_,_,_) <=> nrule(Y).\nred_fai @ nhead(X) \ bodyP(Y,X), rule(Y,_,_,_) <=> nrule(Y).\nred_pos @ nhead(X) \ bodyN(Y,X), rule(Y,P,N,C) <=> A is N-1 | rule(Y,P,A,C).\nred_suc @ fact(X) \ bodyP(Y,X), rule(Y,P,N,C) <=> A is P-1 | rule(Y,A,N,C).\n\nred_con_success @ verified_constraint(X,Y) \ bodyC(X,Y), rule(X,P,N,C) <=> A is C-1 | rule(X,P,N,A).\nred_con_failure @ unsat_constraint(X,Y) \ bodyC(X,Y), rule(X,_,_,_) <=> nrule(X).\nred_unf @ unfounded(U), head(X,H) \ rule(X,_,_,_) <=> memberchk(H,U) | nrule(X).\n\n"
    # Constraint propagation
    constraintPropagation = "%% Constraint propagation\n\n"
    # Empty body
    emptyBody ="%% Empty body \n\nhead(X,Y), rule(X,0,0,0) <=> fact(Y).\n\n"
    # Choice phase

    # choiceRules ="%% Choice\n\n%% The rule is forced to be true.\n%% The negative body cannot be true\nchoi_frule(X), bodyN(X,Y), fact(Y) <=> fail.\nchoi_frule(X) \ bodyC(X,Y) <=> fact(Y).\n\n%% The rule is forced to be false\n%% If one atom from the negative body is true, then fail.\nnhead(Y) \ choi_nrule(X,Z,C), bodyN(X,Y) <=> A is Z-1 | choi_nrule(X,A,C).\n\nchoi_nrule(X,Z,C), verified_constraint(X,_) <=> A is C-1 | choi_nrule(X,Z,A).\nchoi_nrule(_,0,0) <=> fail.\n\nrule(X,0,Z,C), choice(X) <=> (choi_frule(X), rule(X,0,0,0) ; choi_nrule(X,Z,C), nrule(X)).\nenumeration @ dom(X,[V|Rest]) <=> length(Rest,Length), Length =\= 0 | dom(X,[V]) ; dom(X,Rest).\n\n"
    choiceRules = ""
    
    # Printing solutions and fail
    if nbSol == 0:
        printSol = "end <=> chr_show_store(user), write(\".\"), nl, fail.\n"
    elif nbSol == 1:
        printSol = "end <=> chr_show_store(user), write(\".\"), nl.\n"
    else:
        print("ERROR. Cannot translate program for a number of solutions different from 0 or 1. (For now at least... Might be fixed in next version).")
        exit(1)
        
    # Cleaner
    cleaner="%% Cleaner \n\nfact(X) \ fact(X) <=> true.\ncleaner \ bodyP(_,_) <=> true.\ncleaner \ bodyN(_,_) <=> true.\ncleaner \ head(_,_) <=> true.\ncleaner \ bodyC(_,_) <=> true.\ncleaner \ choice(_) <=> true.\ncleaner \ choi_frule(_) <=> true.\ncleaner \ choi_nrule(_,_,_) <=> true.\ncleaner \ nrule(_) <=> true.\ncleaner \ rule(_,_,_,_) <=> true.\ncleaner \ heads(_,_) <=> true.\ncleaner \ verified_constraint(_,_) <=> true.\ncleaner \ unsat_constraint(_,_) <=> true.\n"
    if solveChoicePoint:
        cleaner += "\ncleaner \ nhead(_) <=> true.\n"
        choiceRules ="%% Choice\n\n%% The rule is forced to be true.\n%% The negative body cannot be true\nchoi_frule(X), bodyN(X,Y), fact(Y) <=> fail.\nchoi_frule(X) \ bodyC(X,Y) <=> fact(Y).\n\n%% The rule is forced to be false\n%% If one atom from the negative body is true, then fail.\nnhead(Y) \ choi_nrule(X,Z,C), bodyN(X,Y) <=> A is Z-1 | choi_nrule(X,A,C).\n\nchoi_nrule(X,Z,C), verified_constraint(X,_) <=> A is C-1 | choi_nrule(X,Z,A).\nchoi_nrule(_,0,0) <=> fail.\n\nrule(X,0,Z,C), choice(X) <=> (choi_frule(X), rule(X,0,0,0) ; choi_nrule(X,Z,C), nrule(X)).\nenumeration @ dom(X,[V|Rest]) <=> length(Rest,Length), Length =\= 0 | dom(X,[V]) ; dom(X,Rest).\n\n"
    else :
        choiceRules ="%% Choice\n\n%% The rule is forced to be true.\n%% The negative body cannot be true\nchoi_frule(X), bodyN(X,Y), fact(Y) <=> fail.\n%%choi_frule(X) \ bodyC(X,Y) <=> fact(Y).\n\n%% The rule is forced to be false\n%% If one atom from the negative body is true, then fail.\nnhead(Y) \ choi_nrule(X,Z,C), bodyN(X,Y) <=> A is Z-1 | choi_nrule(X,A,C).\n\n%%choi_nrule(X,Z,C), verified_constraint(X,_) <=> A is C-1 | choi_nrule(X,Z,A).\nchoi_nrule(_,0,0) <=> fail.\n\n%%rule(X,0,Z,C), choice(X) <=> (choi_frule(X), rule(X,0,0,0) ; choi_nrule(X,Z,C), nrule(X)).\n%%enumeration @ dom(X,[V|Rest]) <=> length(Rest,Length), Length =\= 0 | dom(X,[V]) ; dom(X,Rest).\n\n"
    if showSCC:
        cleaner += "%cleaner \ unfounded(_) <=> true.\n%cleaner \ scc_component(_) <=> true.\n%cleaner \ supported(_) <=> true.\n"
    else:
        cleaner += "cleaner \ unfounded(_) <=> true.\ncleaner \ scc_component(_) <=> true.\ncleaner \ supported(_) <=> true.\ncleaner \ nb_support_scc(_,_) <=> true.\ncleaner \ external_support(_,_) <=> true.\n"
    cleaner += "cleaner <=> true.\n\n"

    # Launcher

    launcherBodyP = [] #Contains all the descriptors bodyP/2
    launcherBodyR = [] #Contains all the descriptors bodyN/2, bodyC/2
    launcherRule = [] #Contains all the descriptors rule/2
    launcherHead = [] #Contains all the descriptors head/2, nhead/1
    launcherCons = [] #Contains the constraints
    launcherChoice = [] #Contains all the choice points.
    emptyLauncher = True

    # Adding all the constraint solver to the constraint propagation part
    c_list = [] #contains all the constraints added
    constraint_name = []
    for fileName in os.listdir(dir_path+"/constraints/"):
        filePath = os.path.join(dir_path+"/constraints/", fileName)
        if os.path.isfile(filePath) and fileName[-4:] == ".chr" :
            with open(filePath, 'r') as f:
                for line in f:
                    if line[0] == "#":
                        c_list.append(line[1:-1]) #The line starting with # contains the declaration
                        constraint_name.append(c_list[-1].split("/")[0])
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

    #let's add facts to the launcher
    for f in facts:
        launcherHead.append(str("fact("+f.__str__()+")"))
    
    #let's add domains and facts constraints to the launcher
    for c in constraintFacts:
        launcherCons.append(str(c))

    
    #let's iterate on each rule except the last one.
    for i in range(len(prog)):
        numNeg = 0
        numPos = 0
        numCon = len(prog[i].constraints)
        
        for b in prog[i].body:
            if b.sign:
                numPos = numPos + 1
            else:
                numNeg = numNeg + 1 
        launcherRule.append("rule(" + str(ruleNumber) + "," + str(numPos) + "," + str(numNeg) + "," + str(numCon) + ")")
        launcherHead.append("head("+ str(ruleNumber) + "," + prog[i].head.__str__() + ")")

        if len(prog[i].body) > 0: #if there's no body, do nothing. (empty else)
            #adding positive and negative body to the launcher
            for j in range(len(prog[i].body)):
                appendSymbol(symbols,rules,prog[i].body[j].atom)
                if prog[i].body[j].sign:
                    launcherBodyP.append("bodyP(" + str(ruleNumber) + "," + prog[i].body[j].atom.__str__() + ")")
                    if not isConstraint(prog[i].head):
                        arcArray.append("arc("+prog[i].body[j].atom.__str__()+","+prog[i].head.__str__()+")")
                else:
                    launcherBodyR.append("bodyN(" + str(ruleNumber) + "," + prog[i].body[j].atom.__str__() + ")")
            appendSymbol(symbols,rules,prog[i].body[-1].atom)
        #adding constraints to the launcher
        if len(prog[i].constraints) > 0:
            for j in range(len(prog[i].constraints)):
                launcherBodyR.append("bodyC(" + str(ruleNumber) + "," + prog[i].constraints[j].name + ")")
            
        #emptyBody += "rule(" + str(ruleNumber) + ",0) <=> fact(" + prog[i].head.__str__() + ").\n"
        exampleProg += "%% @r" + str(ruleNumber) + "  " + prog[i].__str__()  + "\n"
        if not isinstance(prog[i].head,Constraint):
            appendSymbolsTable(symbols,rules,prog[i].head.atom,ruleNumber)
        ruleNumber += 1
 
    # symbols = [a] and rules = [[1,2,3]] means that a appears in the rules 1,2,3
    for i in range(len(symbols)):
        if rules[i] != []:
            launcherHead.append("heads(" + symbols[i].__str__() + "," + str(len(rules[i])) + ")")
        else:
            if not symbols[i].__str__() in factSet:
                launcherHead.append("nhead(" + symbols[i].__str__() + ")")

    if solveChoicePoint:
        for i in range(1,ruleNumber):
            if not prog[i-1].isIntegrityConstraint():
                launcherChoice.append("choice(" + str(i) + ")")
    
    listArc = '['+','.join(arcArray)+']'
    symbolsStr = map(lambda x: x.__str__(),symbols)
    listNode = '['+','.join(symbolsStr)+']'

    launcher = "launcher <=> " + ', '.join(launcherHead)

    if len(launcherHead) >= 1:
        launcher += ', '


    if len(launcherBodyP) >= 1:
        launcher += ', '.join(launcherBodyP)
        launcher += ', '
    launcher+="init_sccs("+listNode+","+listArc+")"

    if len(launcherBodyR) + len(launcherCons) + len(launcherRule) >= 1:
        launcher+=', '
        launcher+=', '.join(launcherBodyR + launcherCons + launcherRule)

    if len(launcherChoice) >= 1:
        launcher += ', '
        launcher+=', '.join(launcherChoice)

    if cleanOutput:
        launcher += ", cleaner"
    launcher += ", end.\n"
    headOfRules += "\n"

    #sccComputation = 'init_sccs(Node,Arcs) :- nodes_arcs_sccs(Node, Arcs, Ss), assert_sccs(Ss).\nassert_sccs([]).\nassert_sccs([Comp|Rest]) :- scc_component(Comp), assert_sccs(Rest).\n'
    unfounded = '%%Computing unfounded sets of the program based on the SCCs.\n\n:- chr_constraint scc_component/1, support/2, external_support/2, nb_support_scc/2, nb_support_scc_init/2, supported/1, unfounded/1.\n\ninit_sccs(Node,Arcs) :- nodes_arcs_sccs(Node, Arcs, Ss), assert_sccs(Ss).\nassert_sccs([]).\nassert_sccs([Comp|Rest]) :- scc_component(Comp), assert_sccs(Rest).\n\nhead(X,B), scc_component(SCC) ==> memberchk(B,SCC) | support(X,SCC). %% Compute the support for each SCC.\nbodyP(X,B) \ support(X,SCC) <=> memberchk(B,SCC) | true. %% Deletes all non external support. (to detect loops)\n\nscc_component(SCC) ==> nb_support_scc_init(SCC,0).\n\nsupport(X,SCC), nb_support_scc_init(SCC,N) <=> NewN is N+1 | external_support(X,SCC), nb_support_scc_init(SCC,NewN).\n\nsupported(SCC) \ external_support(_,SCC) <=> true.\nfact(F) \ nb_support_scc(SCC,_) <=> memberchk(F,SCC) | supported(SCC).\n\nnrule(X) \ external_support(X,SCC), nb_support_scc(SCC,N) <=> NewN is N-1 | nb_support_scc(SCC,NewN). %% Remove deleted supports.\n\nnb_support_scc_init(A,B) <=> nb_support_scc(A,B). %% All the supports have been computed.\nnb_support_scc(SCC,0) <=> unfounded(SCC). %% If a SCC has no support, then it\'s unfounded.\n'


    exampleProg += '%% Facts of the program : \n%% ' + '\n%% '.join(factSet) + '\n\n'
    #':- init_sccs('+listNode+','+listArc+').'
    #print(header)
    #print(exampleProg)
    #print(headOfRules)
    #print(transformation)
    #print(emptyBody)
    #print(cleaner)
    #print(launcher)
    
    #return header + exampleProg + headOfRules + transformation + emptyBody + choiceRules + launcher + cleaner + printSol
    return header + exampleProg + headOfRules + unfounded + constraintDeclaration + constraintPropagation + transformation + emptyBody + choiceRules + launcher + cleaner + printSol
