import os
from ReadSummary import *
from CleanSentence import *
from CleanOutput import *
def ReturnReturner(FunctionsFolder,FunctionsListDF):
    FunctionOutputs=[]
    for File in os.listdir(FunctionsFolder):
        FileLoc=FunctionsFolder+'/'+File
        FunctionName=File.replace('.py','')
        FunctionID=int(FunctionsListDF['ID'][FunctionName])
        try:
            Text=ReadSummary(FileLoc)
            for line in Text:
                output=CleanSentence(line,startKey="return ",endKey='\n')
                if output!=0:
                    try:
                        output=CleanOutput(output)
                        FunctionOutputs.append([FunctionName,output])
                    except:
                        print(output)
        except:
            print(File)
    return FunctionOutputs
