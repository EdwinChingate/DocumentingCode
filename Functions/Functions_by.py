import pandas as pd
def Functions_by(function_name,FunctionsMatDF,Head='## Functions\n',start='- [[',end=']]'):    
    MyFunctionLoc=FunctionsMatDF[function_name]==1
    functionsSerie=pd.Series(FunctionsMatDF[MyFunctionLoc].index)
    functionsListLink=start+functionsSerie+end
    FunctionsText=Head+''.join(functionsListLink)
    return FunctionsText
