class Variable:
    def __init__(self, name):
        self.name = name
        
    def __hash__(self):
        # return hash((self.name, self.sign, self.parameters))
        return hash(self.__str__())

    def __eq__(self, other):
        return self.name == other.name
    
    def __str__(self):
        return self.name


class Atom:
    def __init__(self, name, parameters=None):
        self.name = name
        self.parameters = parameters or list()

    def __hash__(self):
        # return hash((self.name, self.sign, self.parameters))
        return hash(self.__str__())

    def __eq__(self, other):
        return self.name == other.name and self.parameters == other.parameters
    
    def __str__(self):
        return self.name + (('(' + ','.join(map(str, self.parameters)) + ')') if len(self.parameters) != 0 else '')

class Constraint: #CP constraint
    def __init__(self, name, variables=None):
        self.name = name
        self.variables = variables or list() #list of string

    def __hash__(self):
        # return hash((self.name, self.sign, self.variables))
        return hash(self.__str__())

    def __eq__(self, other):
        return self.name == other.name and self.variables == other.variables
    
    def __str__(self):
        return self.name + (('(' + ','.join(self.variables) + ')') if len(self.variables) != 0 else '')


class Literal:
    def __init__(self, atom, sign=True):
        self.atom = atom
        self.sign = sign

    def __str__(self):
        return ('not ' if not self.sign else '') + self.atom.__str__()

    def __eq__(self, other):
        return self.atom == other.atom and self.sign == other.sign

    def __hash__(self):
        # return hash((self.name, self.sign, self.variables))
        return hash(self.__str__())


class Rule:
    def __init__(self, head, body, constraints):
        self.head = head
        self.body = body
        self.constraints = constraints
        self.integrityConstraint = (head.__str__() == "bot") #True only if the head = bot 

    def isIntegrityConstraint(self):
        return self.integrityConstraint
    
    def __eq__(self, other):
        if len(self.body) == len(other.body):
            if self.head != other.head:
                return False
            for i in range(len(self.body)):
                if self.body[i] != other.body[i]:
                    return False
            return True
        else:
            return False 

    def __str__(self):            
        #return ', '.join(map(str, self.head)) + " :- " + ', '.join(str(lit) for lit in self.body) + ((", ") if (len(self.body) > 0 and len(self.constraints) > 0) else "") +  ', '.join(str(lit) for lit in self.constraints) + "#" + str(len(self.body)+len(self.constraints))
        return self.head.__str__() + " :- " + ', '.join(str(lit) for lit in self.body) + ((", ") if (len(self.body) > 0 and len(self.constraints) > 0) else "") +  ', '.join(str(lit) for lit in self.constraints) + "#" + str(len(self.body)+len(self.constraints))


# class PartialInterpretation:
#     def __init__(self, I=set(), J=set()):
#         self._I = I
#         self._J = J

#     def __eq__(self, other):
#         return self._I == other._I and self._J == other._J
    
#     def __str__(self):
#         return str(self._I) + str(self._J)


# head = Literal(Atom("p", variables=['X','Y']))
# body = [Literal(Atom("q",variables=['X'])), Literal(Atom("r",variables=['Y']),False)]
# rule = Rule(head, body)

# print( "Here's a rule : ", rule)

# # Output : p(X,Y) :- q(X), not r(Y)
