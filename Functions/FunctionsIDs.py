import os
import pandas as pd
import numpy as np
def FunctionsIDs(FunctionsFolder):
    FunctionsList=[]
    for File in os.listdir(FunctionsFolder):
        FunctionsList.append(File.replace('.py',''))
    NFunctions=len(FunctionsList)
    FunctionsListDF=pd.DataFrame()#[,np.zeros(NFunctions)])
    FunctionsListDF.index=FunctionsList
    FunctionsListDF['ID']=np.arange(NFunctions)
    FunctionsListDF['Documentation']=np.zeros(NFunctions)
    return FunctionsListDF
