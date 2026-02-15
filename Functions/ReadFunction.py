from ReadSummary import *
def ReadFunction(function_name,FunctionsFolder,start='## Code\n\n```python\n',end='\n```'):
    try:
        FileLoc=FunctionsFolder+'/'+function_name+'.py'
        Text=ReadSummary(FileLoc)
        PlainCode=start+''.join(Text)+end
        return PlainCode
    except:
        return ''
