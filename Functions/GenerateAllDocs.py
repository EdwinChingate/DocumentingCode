from GenerateDocFile import *

def GenerateAllDocs(FunctionsMatDF, FunctionsInputsDF, FunctionsOutputsDF, FunctionsFolder, SaveFolder, prefix="ms2Topo_", DescriptionsDict=None):
    if DescriptionsDict is None:
        DescriptionsDict = {}
        
    DocPaths = {}
    FunctionsList = list(FunctionsMatDF.columns)
    
    for function_name in FunctionsList:
        desc = DescriptionsDict.get(function_name, "")
        
        # Generate the file and save the path
        path = GenerateDocFile(
            function_name=function_name, 
            FunctionsMatDF=FunctionsMatDF, 
            FunctionsInputsDF=FunctionsInputsDF, 
            FunctionsOutputsDF=FunctionsOutputsDF, 
            FunctionsFolder=FunctionsFolder, 
            SaveFolder=SaveFolder, 
            prefix=prefix, 
            description=desc
        )
        DocPaths[function_name] = path
        
    return DocPaths
