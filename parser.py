from structure import *

#def parse_asp_old(prog_asp, verbose=False):
    #if verbose:
        #print("Beginning Parsing")
        #print()
    #prog_asp = prog_asp.split('\n')
    #if verbose:
        #print("Array :")
        #print(prog_asp)

    #rules = list()
    #facts = list()
    #constraints = list() #ASP's constraints

    #for line in prog_asp:
        #line = line.strip()
        #if not line or line[0] == "%":
            #if verbose:
                #print("Empty or comment")
            #continue
        #line = line.split('.')[0] # get rid of the comments
        #line = line.split('%')[0] # get rid of the comments
        #if verbose:
            #print("    Line :")
            #print("   ", line)
            
        #parts = line.split(":-") #split the line on the sign ":-". the first part = head and second part = body.
        
        #h = [] #head array 
        #b = [] #body array

        #h = parts[0]
        
        #if len(parts) == 2:
            #b = parts[1]
        
        #if verbose:
            #print("        Head : ")
            #print("        ", h)
            #print("        Body : ")
            #print("        ", b)

        #head = [] #Contains all atoms of the head
        #body = [] #Contains all atoms of the body
        #bodyC = [] #Contains all constraints of the body

        #for i in h.split(','):
            #if i[0] == "#":
                #body.append(Constraint(i[1:]))
            #else:
                #head.append(Literal(Atom(i.strip())))

        #if b:
            #for i in b.split(","):
                #i = i.strip()
                #if i == ",":
                    #continue
                #if i.startswith("not "): 
                    #body.append(Literal(Atom(i[4:]), False))
                #elif i[0] == "#":
                    #body.append(Constraint(i[1:]))
                #elif i != "":
                    #body.append(Literal(Atom(i), True))
                #else:
                    #print("trying to add : ", i, " unsucessfully.")
        
        #if len(h) == 0:
            #this is a constraint
            #pass 
        #elif len(b) == 0:
            #facts.append(head[0])#there should be only one atom in the head in this case
            #pass 
        #else:
            #rules.append(Rule(head[0],body,bodyC))

    #return rules, facts, constraints


import re

def partial_parsing(inputString):
    paren_count = 0
    arity=[]
    atoms=[]
    terms=[]
    constraints=[]
    
    negated = True #True only if there's a not.
    while len(inputString) > 0:
        if inputString[0].isalpha(): #The first character is a letter
                #variable
            if inputString[0].isupper(): #if it starts with an uppercase letter it's a variable
                match = re.search('[A-Z]\w*',inputString)
                atoms.append(Variable(match.group()))
                inputString = inputString[match.end():]
                #since Variables are only in a predicate, it means that we need to add it to the arity of the upper predicate.
                if len(arity) > 0:
                    arity[-1] += 1
                else:
                    print("ERROR. Trying to add a variable, but where ? ")
                arity.append(0) # The variable is of arity 0
            #negated literal
            elif inputString[:4] == "not ":
                negated = False
                inputString = inputString[4:]
            #atom name
            else:
                match = re.search('[a-z]\w*',inputString)
                #we have an atom identifier
                atoms.append(Atom(match.group()))
                if len(arity) > 0:
                    arity[-1] += 1
                arity.append(0)
                inputString = inputString[match.end():]
        elif inputString[0].isnumeric(): #detects number
            match = re.search('[0-9]+',inputString)
            atoms.append(Variable(match.group()))
            if len(arity) > 0:
                arity[-1] += 1
            else:
                print("ERROR. Trying to add a variable, but where ? ")
            arity.append(0) # The variable is of arity 0
            inputString = inputString[match.end():]
        elif inputString[0:2] == "#(":
            par_c = 1
            index = 2
            while par_c != 0 and index < len(inputString):
                if inputString[index] == ')':
                    par_c -= 1
                if inputString[index] == '(':
                    par_c += 1
                index += 1
            constraints.append(Constraint(inputString[2:index-1]))
            inputString = inputString[index:]
            if len(inputString) != 0 and (inputString[0] == ',' or inputString[0] == '.'):
                inputString = inputString[1:]
            if paren_count > 0:
                if len(arity) > 0:
                    arity[-1] += 1
                else:
                    print("A strange bug occured...")
        elif inputString[0] == '(':
            paren_count += 1
            inputString = inputString[1:]
        elif inputString[0] == ")": #End of parameters list. 
            paren_count -= 1
            #pop the pile
            #Take the arity[-1] and put all the terms in the atom coresponding.
            param = [] #temporary list that contains the parameters of the atom.
            if len(arity) > 0:
                terms.append(atoms.pop())
                arity.pop()
                for i in range(arity[-1]):
                    param.append(terms.pop())
                param.reverse()
                atoms[-1].parameters = param
            #terms.append(atoms.pop())
            inputString = inputString[1:]
        elif inputString[0] == ',' or inputString[0] == '.':
            #create new atom !
            if paren_count == 0: #we are not in the parameters of an atom here.
                terms.append(Literal(atoms.pop(),negated))
                arity.pop()
                negated = True
            elif len(atoms) > 0 and len(arity) > 0:
                terms.append(atoms.pop())
                arity.pop()
            if len(atoms) != len(arity):
                print("BUG ! ")
            inputString = inputString[1:]
        elif inputString[0]==" ":
            #this is a fact or empty space
            inputString = inputString[1:]
        else:
            print("Something went wrong during parsing at symbol ", inputString[0])
            exit(1)
    #create a new rule
    #rules.append(head,body,bodyC)
    while len(atoms) > 0:
        #Let's assume all the atoms left are well formed
        #If there's atoms left in the pile, it means that we need to finish them. 
        if paren_count == 0: #we are not in the parameters of an atom here.
            terms.append(Literal(atoms.pop(),negated))
            negated = True
        else:
            terms.append(atoms.pop())
    return terms, constraints
    #print("head : ", atomList)
    #for i in atomList:
        #print(i.__str__())
    

def parse_asp(prog_asp, verbose=False):
    if verbose:
        print("Beginning Parsing")
        print()
    prog_asp = prog_asp.split('\n')
    if verbose:
        print("Array :")
        print(prog_asp)

    rules = list()
    facts = list()
    constraints = list() #ASP's constraints

    for line in prog_asp:
        line = line.strip()
        if not line or line[0] == "%":
            if verbose:
                print("Empty or comment")
            continue
        #line = line.split('.')[0]
        line = line.split('%')[0] # get rid of the comments
        if verbose:
            print("    Line :")
            print("   ", line)
            
        parts = line.split(":-") #split the line on the sign ":-". the first part = head and second part = body.
        
        h = [] #head array 
        b = [] #body array

        h = parts[0] #Contains the head
        
        if len(parts) == 2: #Contains the body
            b = parts[1]
        
        if verbose:
            print("        Head : ")
            print("        ", h)
            print("        Body : ")
            print("        ", b)

        head = [] #Contains all atoms of the head
        headC = [] #Contains all constraints of the head
        body = [] #Contains all atoms of the body
        bodyC = [] #Contains all constraints of the body

        #First let's deal with the head
        head, headC = partial_parsing(h)
        if len(h) != 0 and h[-1] != '.':
            body, bodyC = partial_parsing(b)
        elif len(h) == 0 and len(b) != 0:
            body, bodyC = partial_parsing(b)
        #if len(b) == 0 and len(h) == 1:
            #if type(h[0]) == Constraint:
                #constraints.append(h[0])
        if len(b) == 0:
            if headC == []:
                facts.append(head[0])
            else:
                facts.append(headC[0])
        elif len(h) == 0: #This is a constraint !
            rules.append(Rule(Literal(Atom('bot'),True),body,bodyC))
        else:
            if headC == []:
                rules.append(Rule(head[0],body,bodyC))
            else:
                rules.append(Rule(headC[0],body,bodyC))
            
    return rules, facts, constraints


""" 
asp_prog='''
a :- b, not c.
    c :- not b. %commentttt
  a.
b.
%comment
'''

# rules, facts, constraints = parse_asp(asp_prog, True)
rules, facts, constraints = parse_asp(asp_prog, False)

print()
print("Parsing finished")

print("Rules : ")

for i in rules:
    print("     ", i)

print("Facts : ")

for i in facts:
    print("     ", i)

print("Constraints : ")
for i in constraints:
    print("     ", i)
 """
