def CleanVar(variable,cut='='):    
    end=variable.find(cut)
    if end==-1:
        end=len(variable)
    CleanVariable=variable[:end]
    CleanVariable=CleanVariable.replace('"','')
    CleanVariable=CleanVariable.replace("'",'')
    CleanVariable=CleanVariable.replace(" ",'')
    CleanVariable=CleanVariable.replace("[",'')
    CleanVariable=CleanVariable.replace("]",'')
    return CleanVariable
