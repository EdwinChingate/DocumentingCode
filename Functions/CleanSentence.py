def CleanSentence(line,startKey="from ",endKey=" import *"):
    MoveStart=len(startKey)
    start=line.find(startKey)+MoveStart
    if start==MoveStart-1:
        return 0
    if endKey==0:
        end=len(line)
    else:
        end=line.find(endKey)
    cleanSentence=line[start:end]
    return cleanSentence
