import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import logging

logging.basicConfig(
    filename='logging/debug.log',
    level=logging.DEBUG,
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def normalisation (df,column_name):
    """
    Normalizes a numeric column in the DataFrame using MinMaxScaler and adds a new column with the normalized values.

    Args:
        df (pd.DataFrame): The DataFrame containing the column to normalize.
        column_name (str): The name of the column to normalize.

    Returns:
        df (pd.DataFrame): DataFrame with an additional column containing the normalized values.
    """
    logging.info("Running normalisation function")
    logging.debug(f"Arguments: column_name={column_name}")

    # Check if the column is numeric
    if not pd.api.types.is_numeric_dtype(df[column_name]):
        logging.error(f"Column '{column_name}' is not numeric. Normalization cannot proceed.")
        raise TypeError('The column must be numeric for normalization.')

    try:
        # Apply MinMaxScaler to normalize the column
        logging.info(f"Normalizing column: {column_name}")
        scaler = MinMaxScaler()
        df[[column_name + '_normalised']] = scaler.fit_transform(df[[column_name]])
        logging.info(f"Successfully normalized column '{column_name}'. Added new column '{column_name}_normalised'.")
        return df

    except Exception as e:
        logging.error(f"Error during normalization: {e}")
        raise
