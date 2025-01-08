import numpy as np
import pandas as pd
from ReturnReturner import *
def FunctionsOutputs(FunctionsFolder,FunctionsListDF):
    NFunctions=len(FunctionsListDF)
    FunctionsVariables=ReturnReturner(FunctionsFolder=FunctionsFolder,FunctionsListDF=FunctionsListDF)
    AllVariables=[]
    for Fun in FunctionsVariables:
        AllVariables=AllVariables+Fun[1]
    OutputVariables=list(set(AllVariables))
    NVariables=len(OutputVariables)
    FunctionsOutputsMat=np.zeros((NVariables,NFunctions))
    FunctionsOutputsDF=pd.DataFrame(FunctionsOutputsMat,index=OutputVariables,columns=FunctionsListDF.index)
    for Fun in FunctionsVariables:
        FunctionsOutputsDF[Fun[0]][Fun[1]]=1
    return FunctionsOutputsDF
