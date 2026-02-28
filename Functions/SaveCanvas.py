import json
def SaveCanvas(Canvas, FilePath):
    with open(FilePath, 'w') as f:
        json.dump(Canvas, f, indent='\t')
    return FilePath
