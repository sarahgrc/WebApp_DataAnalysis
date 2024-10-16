import pandas as pd

def dataframe_concat(df,key):
    #parameters : 
    #df : list with 2 dataframes to concatenate
    #key : name of the column to join the df

    #Verification that df is a list of two dataframes
    if not isinstance(df,list) or len(df)!=2 or not all(isinstance(x, pd.DataFrame) for x in df):
         raise ValueError ('df must be a list with two dataframes')
    
    #Verification that key is a list of one or two column names
    if not isinstance(key,list) or len(key) not in [1,2] :
         raise ValueError ('key must be a list with one or two column names')
    
    #merging the two dataframes 
    if len(key)==1:
          #check key is a column name in both dataframes
          if key[0] not in df[0].columns or key[0] not in df[1].columns:
               raise KeyError(f"The column '{key[0]}' does not exist in one of the DataFrames.")
          else:
               df_merged=pd.merge(df[0],df[1],on=key[0])
    else : 
          #check both keys are a column name in each dataframes
          if key[0] not in df[0].columns or key[1] not in df[1].columns:
               raise KeyError(f"The column '{key[0]}' or '{key[1]}' does not exist in one of the DataFrames.")
          else : 
               df_merged=pd.merge(df[0],df[1], left_on=key[0], right_on=key[1])
               df_merged.drop(key[1],axis=1,inplace=True)
     
    return df_merged
    







