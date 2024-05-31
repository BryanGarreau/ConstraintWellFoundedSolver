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

def generateVariableDeclaration(n):
    program = "%% Creating variables and domains \n\n"
    for i in range(1,n+1):
        program += "#(dom(q" + str(i) + ",["
        for j in range(1,n):
            program += str(j) + ","
        program += str(n) + "]).\n"
    program += "\n"
    return program

def generateAlldiff(n):
    program = "%% Alldifferent\n\n#(alldiff(["
    for j in range(1,n):
        program += "q" + str(j) + ","
    program += "q" + str(n) + "])).\n\n"
    return program

def generateEqualConstraint(n):
    program = "%% Diagonal constraints\n\n"
    for i in range(1,n+1):
        for j in range(1,n+1-i):
            program += "#(nequal(q" + str(i) + ", " + str(j) + ",q" + str(i+j) + ")).\n"
            program += "#(nequal(q" + str(i) + ",-" + str(j) + ",q" + str(i+j) + ")).\n"
    program += "\n"
    return program

print("Creating all the instances.")    
ASPdirectory = "./ASP"
CASPdirectory = "./CASP"

for n in [4,5,6,7]:
    outputFileName = ASPdirectory + "/" + str(n) + "queens.asp"
    fileOutput = open(outputFileName,"w")
    fileOutput.write(generateChoice(n))
    fileOutput.write(generateLineConstraint(n))
    fileOutput.write(generateDiagConstraint(n))
    fileOutput.close()
    outputFileName = CASPdirectory + "/" + str(n) + "queens.casp"
    fileOutput = open(outputFileName,"w")
    fileOutput.write(generateVariableDeclaration(n))
    fileOutput.write(generateAlldiff(n))
    fileOutput.write(generateEqualConstraint(n))
    fileOutput.close()
print("Programs correctly generated ! ")
