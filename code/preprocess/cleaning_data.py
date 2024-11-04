import pandas as pd

def outliers(dataframe, column,treshold_sup=None, treshold_inf=None, get_info=False):
    """
    function that returns a list of all outliers in a column depending on the treshold
    
    Args:
        dataframe : 
        column (string) : name of the column
        treshold_sup (int,float, optional): treshold for the outliers superior to a value. Defaults to None.
        treshold_inf (int,float, optional): treshold for the outliers inferior to a value. Defaults to None.
        get_info (bool, optional): _description_. Defaults to False.

    Returns:
        outliers: list with all outliers 
    """

    #verification that treshold_sup is a value
    if treshold_sup is not None:
        if not isinstance(treshold_sup, (int, float)):
            raise ValueError('treshold_sup must be an int or float')
        
    #verification that treshold_inf is a real value
    if treshold_inf is not None:
        if not isinstance(treshold_inf, (int, float)):
            raise ValueError('treshold_inf must be an int or float')
    
    if get_info : 
        outliers=pd.DataFrame()
        for i in range(len(dataframe[column])):
            if treshold_sup is not None :
                if dataframe[column][i]>treshold_sup: outliers.append(dataframe[column][i].item())
            if treshold_inf is not None :
                if dataframe[column][i]<treshold_inf: outliers.append(dataframe[column][i].item())
        return 

    else :
        outliers_sup=[]
        outliers_inf=[]
        for i in range(len(dataframe[column])):
            if treshold_sup is not None :
                if dataframe[column][i]>treshold_sup: outliers_sup.append(dataframe[column][i].item())
            if treshold_inf is not None :
                if dataframe[column][i]<treshold_inf: outliers_inf.append(dataframe[column][i].item())
    
        if len(outliers_sup)>0 and len(outliers_inf)>0: return outliers_sup,outliers_inf
        elif len(outliers_sup)>0 : return outliers_sup
        elif len(outliers_inf)>0 : return outliers_inf
        else : print('There are no outliers for this column and this treshold')    
