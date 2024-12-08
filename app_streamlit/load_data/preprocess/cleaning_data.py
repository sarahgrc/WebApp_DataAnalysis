import pandas as pd
import copy

def outliers_df(dataframe, column,treshold_sup=None, treshold_inf=None, get_info=False):
    """
    function that returns a list of all outliers in a column depending on the treshold
    
    Args:
        dataframe : 
        column (string) : name of the column
        treshold_sup (int,float, optional): treshold for the outliers superior to a value. Defaults to None.
        treshold_inf (int,float, optional): treshold for the outliers inferior to a value. Defaults to None.
        get_info (bool, optional): _description_. Defaults to False.

    Returns:
        outliers: if get_info is true then dataframe with all outliers else just a list of outliers 
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
        if treshold_sup is not None and treshold_inf is None:
            outliers=dataframe.loc[(dataframe[column] > treshold_sup)]
        if treshold_sup is None and treshold_inf is not None:
            outliers=dataframe.loc[(dataframe[column] < treshold_inf)]
        if treshold_sup is not None and treshold_inf is not None:
            outliers=dataframe.loc[(dataframe[column] > treshold_sup) & (dataframe[column] < treshold_inf)]
        return outliers

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


def date_separated(col_name,dataframe):
    """
    this function takes a column with a date in the string format YYYY-MM-DD and return 
    the dataframe with 3 new columns for the day, month and year 

    Args:
        col_name (string): name of the column with the date in the dataframe 
        dataframe : name of the dataframe 

    Returns:
        dataframe : return the new dataframe with the addition of the extracted informations in 3 columns
    """

    #create a datatime object
    df = dataframe.copy()
    df[col_name] = pd.to_datetime(df[col_name])   

    #create three columns with the day, month and year 
    df['day'] = df[col_name].dt.day
    df['month'] = df[col_name].dt.month
    df['year'] = df[col_name].dt.year

    return df

def add_season(df):
    """ Add a season column to the dataset """
    def get_season(month):
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        elif month in [9, 10, 11]:
            return 'autumn'

    df['season'] = df['month'].map(get_season)
    return df


def remove_outliers_iqr(df, column):
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        inter = q3 - q1
        lower_bound = q1 - 1.5 * inter
        upper_bound = q3 + 1.5 * inter
        return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

