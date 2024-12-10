import pandas as pd
import logging 

logging.basicConfig(
    filename='logging/debug.log',
    level=logging.DEBUG,
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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
     logging.info("Running dataframe_concat function")
     logging.debug(f"Arguments: join={join}, key={key}")

     valid_joins = ["left", "right", "outer", "inner"]
     key_list = key if isinstance(key, list) else [key]

     # Validate join type
     if join not in valid_joins:
        logging.error(f"Invalid join type: {join}. Must be one of {valid_joins}.")
        raise ValueError(f"Invalid join type. Expected one of {valid_joins}, but got {join}.")

    # Verify df is a list of two dataframes
     if not isinstance(df, list) or len(df) != 2 or not all(isinstance(x, pd.DataFrame) for x in df):
        logging.error("df must be a list containing exactly two pandas DataFrames.")
        raise ValueError('df must be a list with two pandas DataFrames.')

    # Verify key is a list or string with valid column names
     if not isinstance(key, (list, str)):
        logging.error("key must be a string or a list of column names.")
        raise ValueError('key must be a string or a list of column names.')

     if len(key_list) not in [1, 2]:
          logging.error("key must contain one or two column names.")
          raise ValueError('key must be a list with one or two column names.')

     try:
        # Merging the dataframes
        if len(key_list) == 1:
            # Check if the key exists in both dataframes
            if key_list[0] not in df[0].columns or key_list[0] not in df[1].columns:
                logging.error(f"The column '{key_list[0]}' does not exist in one of the DataFrames.")
                raise KeyError(f"The column '{key_list[0]}' does not exist in one of the DataFrames.")

            logging.info(f"Merging dataframes on key: {key_list[0]} with join type: {join}")
            df_merged = pd.merge(df[0], df[1], on=key_list[0], how=join)

        else:
            # Check if the keys exist in both dataframes
            if key_list[0] not in df[0].columns or key_list[1] not in df[1].columns:
                logging.error(f"The column '{key_list[0]}' or '{key_list[1]}' does not exist in one of the DataFrames.")
                raise KeyError(f"The column '{key_list[0]}' or '{key_list[1]}' does not exist in one of the DataFrames.")

            logging.info(f"Merging dataframes on keys: {key_list[0]} (left) and {key_list[1]} (right) with join type: {join}")
            df_merged = pd.merge(df[0], df[1], left_on=key_list[0], right_on=key_list[1], how=join)
            df_merged.drop(key_list[1], axis=1, inplace=True)

        logging.info(f"Successfully merged dataframes. Resulting shape: {df_merged.shape}")
        return df_merged

     except Exception as e:
        logging.error(f"Error during dataframe concatenation: {e}")
        raise

    








