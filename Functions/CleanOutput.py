from CleanVar import *
def CleanOutput(line):    
    Variables=line.split(',')
    Var=list(map(CleanVar,Variables))
    return Var
