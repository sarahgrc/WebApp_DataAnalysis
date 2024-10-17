import pandas as pd

def dataframe_concat(df,key,join="left"):
     """
     fonction to merge two dataframes on one column (by default on with a left join). 

     Args:
         df (list): list with 2 dataframes to concatenate
         key (list): name of the column to join the df
         left_join (bool, optional): _description_. Defaults to False.
         right_join (bool, optional): _description_. Defaults to False.
         join (string): left, right, outer, inner

     Raises:
         ValueError: _description_
         ValueError: _description_
         KeyError: _description_
         KeyError: _description_

     Returns:
         _type_: _description_
     """
     valid_joins = ["left", "right", "outer", "inner"]

    #verification that df is a list of two dataframes
     if not isinstance(df,list) or len(df)!=2 or not all(isinstance(x, pd.DataFrame) for x in df):
         raise ValueError ('df must be a list with two dataframes')
    
    #verification that key is a list of one or two column names
     if not isinstance(key,list) or len(key) not in [1,2] :
         raise ValueError ('key must be a list with one or two column names')
    
    #merging the two dataframes 
     if len(key)==1:
          #check key is a column name in both dataframes
          if key[0] not in df[0].columns or key[0] not in df[1].columns:
               raise KeyError(f"The column '{key[0]}' does not exist in one of the DataFrames.")
          else:
               df_merged=pd.merge(df[0],df[1],on=key[0],how=join)
     else : 
          #check both keys are a column name in each dataframes
          if key[0] not in df[0].columns or key[1] not in df[1].columns:
               raise KeyError(f"The column '{key[0]}' or '{key[1]}' does not exist in one of the DataFrames.")
          else : 
               df_merged=pd.merge(df[0],df[1], left_on=key[0], right_on=key[1],how=join)
               df_merged.drop(key[1],axis=1,inplace=True)
     
     return df_merged
    








