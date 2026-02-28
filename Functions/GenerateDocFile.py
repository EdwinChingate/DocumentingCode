import os
from Functions_by import *
from ReadFunction import *

def GenerateDocFile(function_name, FunctionsMatDF, FunctionsInputsDF, FunctionsOutputsDF, FunctionsFolder, SaveFolder, prefix="ms2Topo_", description=""):
    # Pull dependencies and variables
    FunctionsCalled_by = Functions_by(function_name=function_name, FunctionsMatDF=FunctionsMatDF.T, Head='\n## Functions\n\n', start='- [[', end=']]\n')
    FunctionsCalling = Functions_by(function_name=function_name, FunctionsMatDF=FunctionsMatDF, Head='\n## Called by\n\n', start='- [[', end=']]\n')
    FunctionOutputs = Functions_by(function_name=function_name, FunctionsMatDF=FunctionsOutputsDF, Head='\n## Output\n\n', start='- [[', end=']]\n')
    FunctionInputs = Functions_by(function_name=function_name, FunctionsMatDF=FunctionsInputsDF, Head='\n## Input\n\n', start='- [[', end=']]\n')

    PlainCode = ReadFunction(function_name=function_name, FunctionsFolder=FunctionsFolder)

    FunctionsCalling = FunctionsCalling.replace('[[', f'[[{prefix}')
    FunctionsCalled_by = FunctionsCalled_by.replace('[[', f'[[{prefix}')

    Title = '## Description\n\n' + description + '\n'
    key_operations = '' 
    SubTitle = '\n## Parameters\n'
    
    TextList = [Title, key_operations, PlainCode, SubTitle, FunctionInputs, FunctionOutputs, FunctionsCalled_by, FunctionsCalling]
    DocText = '\n---\n'.join([text for text in TextList if text.strip() != ''])

    if not os.path.exists(SaveFolder):
        os.makedirs(SaveFolder)

    SaveName = prefix + function_name
    SavePath = f"{SaveFolder}/{SaveName}.md" 
    
    # Physically save the file
    with open(SavePath, 'w') as TextFile:
        TextFile.write(DocText)

    # ONLY return the filename, we will attach the Vault path in the Canvas step
    return f"{SaveName}.md"
