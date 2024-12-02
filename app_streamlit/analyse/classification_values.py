
def main_values(col_name,col_para_name,parameters,treshold,dataframe):
    """
    this function returns the most important values (for example the top 10 if treshold=10) 
    depending on the value of another column.

    Args:
        col_name (string): name of the column with the values we want
        col_para_name (string): column on which we depend 
        parameters (list, string or int): name of the parameters (if multiple : must be for the same col_para_name)
        treshold (int): max number of values to return
        dataframe : dataframe that is used 

    example : main_values('n_steps','minutes',[55,35],10,raw_recipes) returns the top 10 
    n_steps of recipes that take 55 or 35 minutes to do. 

    Returns:
        top_values : list of dictionnary with values as keys and their count as values
    """

    #verify columns exist in the dataframe
    if col_name not in dataframe.columns or col_para_name not in dataframe.columns:
        raise ValueError("col_name or col_para_name does not exist in the dataframe")

    #verify column names are strings
    if not isinstance(col_name, str) or not isinstance(col_para_name, str):
        raise ValueError("col_name and col_para_name must be strings")

    #verify treshold is an integer
    if not isinstance(treshold, int):
        raise ValueError("treshold must be an integer")
    
    top_values=[]
    
    params = parameters if isinstance(parameters, list) else [parameters]  
    
    for p in params:
        val_counts = dataframe[dataframe[col_para_name] == p][col_name].value_counts().head(treshold)
        #convert val_counts to dictionary and append it the top_values list
        top_values.append(val_counts.to_dict())
    
    return top_values


