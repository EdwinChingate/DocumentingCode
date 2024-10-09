import os
from ReadSummary import *
from CleanVariables import *
def VariablesLists(FunctionsFolder,FunctionsListDF):
    FunctionsVariables=[]
    for File in os.listdir(FunctionsFolder):
        FileLoc=FunctionsFolder+'/'+File
        FunctionName=File.replace('.py','')
        FunctionID=int(FunctionsListDF['ID'][FunctionName])
        Text=ReadSummary(FileLoc)
        for line in Text:
            Var=CleanVariables(line)
            if Var!=0:
                FunctionsVariables.append([FunctionName,Var])
    return FunctionsVariables
