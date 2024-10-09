def ReadSummary(textName):
    Text = open(textName, "r")
    TextLines=Text.readlines()
    Text.close()
    return TextLines
