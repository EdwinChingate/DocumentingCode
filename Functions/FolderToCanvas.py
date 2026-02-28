import numpy as np
import pandas as pd
from FunctionsIDs import *
from FillFunctionsMat import *
from FunctionsInputs import *
from FunctionsOutputs import *
from GenerateAllDocs import *
from TreeToCanvas import *
from SaveCanvas import *

def FolderToCanvas(FunctionsFolder, SaveFolder, OutputCanvasPath, VaultDocPath, prefix="ms2Topo_"):
    FunctionsListDF = FunctionsIDs(FunctionsFolder)
    NFunctions = len(FunctionsListDF)

    FunctionsMat = np.zeros((NFunctions, NFunctions))
    FunctionsMat = FillFunctionsMat(FunctionsFolder, FunctionsMat, FunctionsListDF)
    FunctionsMatDF = pd.DataFrame(FunctionsMat, index=FunctionsListDF.index, columns=FunctionsListDF.index)

    FunctionsInputsDF = FunctionsInputs(FunctionsFolder, FunctionsListDF)
    FunctionsOutputsDF = FunctionsOutputs(FunctionsFolder, FunctionsListDF)

    print("Generating Markdown documentation...")
    DocPaths = GenerateAllDocs(
        FunctionsMatDF=FunctionsMatDF, 
        FunctionsInputsDF=FunctionsInputsDF, 
        FunctionsOutputsDF=FunctionsOutputsDF, 
        FunctionsFolder=FunctionsFolder, 
        SaveFolder=SaveFolder,
        prefix=prefix
    )

    print("Generating Canvas map...")
    # Pass VaultDocPath here!
    Canvas = TreeToCanvas(FunctionsMatDF, DocPaths, VaultDocPath, node_width=800, node_height=600, h_gap=200, v_gap=400)

    SaveCanvas(Canvas, OutputCanvasPath)
    print(f"Done! Canvas saved to {OutputCanvasPath}")
    
    return Canvas
