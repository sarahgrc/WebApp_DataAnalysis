import logging 
import os 

log_dir = "logging"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir,'debug.log'),
    level=logging.DEBUG,
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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

    logging.info("Running main_values function")
    logging.debug(f"Arguments: col_name={col_name}, col_para_name={col_para_name}, parameters={parameters}, treshold={treshold}")

    # Verify that columns exist in the DataFrame
    if col_name not in dataframe.columns or col_para_name not in dataframe.columns:
        logging.error(f"Columns '{col_name}' or '{col_para_name}' do not exist in the DataFrame.")
        raise ValueError("col_name or col_para_name does not exist in the DataFrame")

    # Verify column names are strings
    if not isinstance(col_name, str) or not isinstance(col_para_name, str):
        logging.error("col_name and col_para_name must be strings.")
        raise ValueError("col_name and col_para_name must be strings")

    # Verify treshold is an integer
    if not isinstance(treshold, int):
        logging.error("treshold must be an integer.")
        raise ValueError("treshold must be an integer")

    try:
        # Initialize results list
        top_values = []

        # Normalize parameters to a list
        params = parameters if isinstance(parameters, list) else [parameters]

        logging.info(f"Analyzing parameters: {params}")

        for p in params:
            logging.debug(f"Processing parameter: {p}")
            val_counts = dataframe[dataframe[col_para_name] == p][col_name].value_counts().head(treshold)
            logging.info(f"Top {treshold} values for parameter '{p}' in '{col_para_name}': {val_counts.to_dict()}")
            # Convert value counts to dictionary and append to top_values list
            top_values.append(val_counts.to_dict())

        logging.info("Successfully calculated top values.")
        return top_values

    except Exception as e:
        logging.error(f"Error in main_values: {e}")
        raise

