import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def normalisation (df,column_name):
    if not pd.api.types.is_numeric_dtype(df[column_name]):  
        return print('Take a numeric colomun ')
    else : 
        scaler=MinMaxScaler()
        df[[column_name + '_normalisé']] = scaler.fit_transform(df[[column_name]])
        return df
