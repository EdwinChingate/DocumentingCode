import numpy as np
import pandas as pd
from FunctionsIDs import *
from FillFunctionsMat import *
from MatToCanvas import *
from SaveCanvas import *

def FolderToCanvas(FunctionsFolder, OutputPath, node_width=400, node_height=200, h_gap=100, v_gap=400):
    # Step 1: Index all functions
    FunctionsListDF = FunctionsIDs(FunctionsFolder)
    NFunctions = len(FunctionsListDF)

    # Step 2: Build adjacency matrix
    FunctionsMat = np.zeros((NFunctions, NFunctions))
    FunctionsMat = FillFunctionsMat(FunctionsFolder, FunctionsMat, FunctionsListDF)

    # Step 3: Convert to labeled DataFrame
    FunctionsMatDF = pd.DataFrame(
        FunctionsMat,
        index=FunctionsListDF.index,
        columns=FunctionsListDF.index
    )

    # Step 4: Generate canvas
    Canvas = MatToCanvas(FunctionsMatDF, node_width, node_height, h_gap, v_gap)

    # Step 5: Save
    SaveCanvas(Canvas, OutputPath)
    return Canvas
