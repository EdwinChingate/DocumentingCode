from CleanVar import *
def CleanVariables(line,startKey="def ",middleKey="(",endKey="):"):
    MoveStart=len(startKey)
    start=line.find(startKey)+MoveStart
    if start==MoveStart-1:
        return 0
    if endKey==0:
        end=len(line)
    else:
        end=line.find(endKey)
    middle=line.find(middleKey)+1
    cleanSentence=line[middle:end]
    Variables=cleanSentence.split(',')
    Var=list(map(CleanVar,Variables))
    return Var
