import pandas as pd

def dataframe_concat(df,key,join="left"):
     """
     fonction to merge two dataframes on one column (by default with a left join).

     Args:
         df (list): list with 2 dataframes to concatenate
         key (list): name of the column(s) to join the df
         join (string) : type of the join (left, right, outer, inner)

     Returns:
         df_merged: new dataframe merged on 1 or more columns with a specific join
     """
     valid_joins = ["left", "right", "outer", "inner"]
     key_list = key if isinstance(key, list) else [key]

    #verification that df is a list of two dataframes
     if not isinstance(df,list) or len(df)!=2 or not all(isinstance(x, pd.DataFrame) for x in df):
         raise ValueError ('df must be a list with two dataframes')

    #verification that key is a list of one or two column names
     if not isinstance(key,list) and not isinstance(key,str) or len(key_list) not in [1,2] :
         raise ValueError ('key must be a list with one or two column names')

    #merging the two dataframes
     if len(key_list)==1:
          #check key is a column name in both dataframes
          if key_list[0] not in df[0].columns or key_list[0] not in df[1].columns:
               raise KeyError(f"The column '{key_list[0]}' does not exist in one of the DataFrames.")
          else:
               df_merged=pd.merge(df[0],df[1],on=key_list[0],how=join)
     else :
          #check both keys are a column name in each dataframes
          if key_list[0] not in df[0].columns or key_list[1] not in df[1].columns:
               raise KeyError(f"The column '{key_list[0]}' or '{key_list[1]}' does not exist in one of the DataFrames.")
          else :
               df_merged=pd.merge(df[0],df[1], left_on=key_list[0], right_on=key_list[1],how=join)
               df_merged.drop(key_list[1],axis=1,inplace=True)

     return df_merged

    








