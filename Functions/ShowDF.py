from IPython.display import HTML, display
import tabulate	
import pandas as pd
def ShowDF(DF,col=''):
    if type(DF)!=type(pd.DataFrame()):
        DF=pd.DataFrame(DF)
    if col=='':
        col=list(DF.columns)
    display(HTML(tabulate.tabulate(DF[col], headers= col,tablefmt='html')))    
