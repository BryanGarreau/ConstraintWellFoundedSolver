import sys

def generateChoice(n):
    program = ""
    for i in range(1,n+1):
        for j in range(1,n+1): 
            program += "q("+ str(i) +"," + str(j) + ") :-"
            for k in range(1,n+1):
                if k != j:
                    program += " not q(" + str(i) + ","+ str(k) + ")"
                    if j != n and k < n:
                        program += ","
                    elif j == n and k < n-1:
                        program += ","
                    
            program += ".\n"
        program += "\n"
    return program

def generateLineConstraint(n):
    program = "% Line Constraints \n"
    for line in range(1,n+1):
        for i in range(1,n+1):
            for j in range(i+1,n+1):
                program += ":- q(" + str(i) + "," + str(line) + "), q(" + str(j) + "," + str(line) + ").\n"
        program += "\n"
    return program

def generateDiagConstraint(n):
    program = "% Diag Constraints \n"
    for col in range(1,n+1):
        for line in range(1,n+1):
            for i in range(1,n+1-col):
                if col + i <= n:
                    if line + i <= n:
                        program += ":- q(" + str(col) + "," + str(line) + "), q(" + str(col+i) + "," + str(line+i) + ").\n" 
                    if line - i > 0:
                        program += ":- q(" + str(col) + "," + str(line) + "), q(" + str(col+i) + "," + str(line-i) + ").\n"
            
        program += "\n"
    return program


if len(sys.argv) == 1:
    n = 4 # default value for queen number
elif len(sys.argv) == 2:
    n = int(sys.argv[1])
else:
    print("There is a problem in the arguments... Only one argument expected (number of queens)")
    
directory = "./ASP"

outputFileName = directory + "/" + str(n) + "queens.asp"
fileOutput = open(outputFileName,"w")
fileOutput.write(generateChoice(n))
fileOutput.write(generateLineConstraint(n))
fileOutput.write(generateDiagConstraint(n))
fileOutput.close()

print("Program generated ! ")
