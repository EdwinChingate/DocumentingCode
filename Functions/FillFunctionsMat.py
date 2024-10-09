import os
from ReadSummary import *
from CleanSentence import *
def FillFunctionsMat(FunctionsFolder,FunctionsMat):
    for File in os.listdir(FunctionsFolder):
        FileLoc=FunctionsFolder+'/'+File
        FunctionName=File.replace('.py','')
        FunctionID=int(FunctionsListDF['ID'][FunctionName])
        Text=ReadSummary(FileLoc)
        for line in Text:
            function=CleanSentence(line,startKey="from ",endKey=" import *")
            if function!=0:
                try:
                    CalledFunctionID=int(FunctionsListDF['ID'][function])
                    FunctionsMat[FunctionID,CalledFunctionID]=1
                except:
                    print(function)
    return FunctionsMat