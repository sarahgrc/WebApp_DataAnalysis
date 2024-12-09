import pandas as pd 
import logging

logging.basicConfig(filename='logging/debug.log', level=logging.DEBUG, filemode="w", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def add_columns(df_target, df_source, key_target, key_source, columns_to_add):
    """
    Adds specified columns from a source DataFrame to a target DataFrame using specified keys,
    without including the key column from the source DataFrame in the final DataFrame and avoiding unwanted columns.

    Args:
    df_target (pd.DataFrame): Target DataFrame where the columns will be added.
    df_source (pd.DataFrame): Source DataFrame containing the columns to be added.
    key_target (str): Name of the key column in the target DataFrame.
    key_source (str): Name of the key column in the source DataFrame.
    columns_to_add (list): List of columns to add from the source DataFrame.

    Returns:
    pd.DataFrame: The target DataFrame with the new columns added.
    """

    try : 
        logging.info("Starting add_columns function.")
    # Checking key columns
        if key_target not in df_target.columns:
            error_message = f"The key '{key_target}' is not in the output dataframe."
            logging.error(error_message)
        if key_source not in df_source.columns:
            error_message = f"The key '{key_target}' is not in the intput dataframe."
            logging.error(error_message)

        # Checking the columns to add
        missing_cols = [col for col in columns_to_add if col not in df_source.columns]
        if missing_cols:
            error_message = f"The following columns are missing in the source DataFrame : {missing_cols}"
            logging.error(error_message)

        # Select only the necessary columns from the source DataFrame
        df_source_reduced = df_source[[key_source] + columns_to_add].copy()

        # Remove the 'id' column from the target DataFrame if it is not the join key
        if key_source in df_target.columns and key_source != key_target:
            df_target = df_target.drop(columns=[key_source])

        # Perform the merge without creating 'id_x' or 'id_y' columns
        df_result = pd.merge(
            df_target,
            df_source_reduced,
            left_on=key_target,
            right_on=key_source,
            how='left'
        )

        # Remove key column from source DataFrame after merge only if it is different from key_target. 
        if key_source != key_target:
            df_result = df_result.drop(columns=[key_source])
        
        logging.info("add_columns function completed successfully.")
        return df_result

    except Exception as e:
        logging.exception("An error occurred in add_columns.")
        raise

def drop_columns(df, columns_to_drop):
    """
    Function that drops columns.

    Args:
        df : dataframe
        columns_to_drop (list, string): name of the column(s) to drop

    Returns:
        df: new dataframe without the columns that weren't needed
    """
    try:
        logging.info("Starting drop_columns function.")

        if not isinstance(df, pd.DataFrame):
            error_message = "The input must be a DataFrame."
            logging.error(error_message)
            raise ValueError(error_message)

        columns_to_drop = columns_to_drop if isinstance(columns_to_drop, list) else [columns_to_drop]

        for col in columns_to_drop:
            if col not in df.columns:
                logging.warning(f"Column '{col}' not found in the DataFrame. Skipping.")
                continue
            logging.info(f"Dropping column: {col}")
            df = df.drop(col, axis=1)

        logging.info("drop_columns function completed successfully.")
        return df

    except Exception as e:
        logging.exception("An error occurred in drop_columns.")
        raise