import numpy as np
import pandas as pd
from VariablesLists import *
def FunctionsInputs(FunctionsFolder,FunctionsListDF):
    NFunctions=len(FunctionsListDF)
    FunctionsVariables=VariablesLists(FunctionsFolder=FunctionsFolder,FunctionsListDF=FunctionsListDF)
    AllVariables=[]
    for Fun in FunctionsVariables:
        AllVariables=AllVariables+Fun[1]
    InputVariables=list(set(AllVariables))
    NVariables=len(InputVariables)
    FunctionsInputsMat=np.zeros((NVariables,NFunctions))
    FunctionsInputsDF=pd.DataFrame(FunctionsInputsMat,index=InputVariables,columns=FunctionsListDF.index)
    for Fun in FunctionsVariables:
        FunctionsInputsDF[Fun[0]][Fun[1]]=1
    return FunctionsInputsDF
