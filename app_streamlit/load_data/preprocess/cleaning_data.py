import pandas as pd
import logging
import copy

logging.basicConfig(
    filename='logging/debug.log',
    level=logging.DEBUG,
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def outliers_df(dataframe, column, treshold_sup=None, treshold_inf=None, get_info=False):
    """
    Function that returns a list of all outliers in a column depending on the threshold.

    Args:
        dataframe : pandas.DataFrame
        column (string) : name of the column
        treshold_sup (int,float, optional): threshold for the outliers superior to a value. Defaults to None.
        treshold_inf (int,float, optional): threshold for the outliers inferior to a value. Defaults to None.
        get_info (bool, optional): If True, returns a dataframe with all outliers else just a list of outliers. Defaults to False.

    Returns:
        outliers: DataFrame or list of outliers based on `get_info`.
    """
    logging.info("Running outliers_df function")
    logging.debug(f"Arguments: column={column}, treshold_sup={treshold_sup}, treshold_inf={treshold_inf}, get_info={get_info}")

    # Verification of threshold_sup
    if treshold_sup is not None:
        if not isinstance(treshold_sup, (int, float)):
            logging.error("treshold_sup must be an int or float")

    # Verification of threshold_inf
    if treshold_inf is not None:
        if not isinstance(treshold_inf, (int, float)):
            logging.error("treshold_inf must be an int or float")

    if get_info:
        outliers = pd.DataFrame()
        if treshold_sup is not None and treshold_inf is None:
            outliers = dataframe.loc[(dataframe[column] > treshold_sup)]
        if treshold_sup is None and treshold_inf is not None:
            outliers = dataframe.loc[(dataframe[column] < treshold_inf)]
        if treshold_sup is not None and treshold_inf is not None:
            outliers = dataframe.loc[(dataframe[column] > treshold_sup) & (dataframe[column] < treshold_inf)]
        logging.info(f"Found {len(outliers)} outliers with get_info=True")
        return outliers

    else:
        outliers_sup = []
        outliers_inf = []
        for i in range(len(dataframe[column])):
            if treshold_sup is not None:
                if dataframe[column][i] > treshold_sup:
                    outliers_sup.append(dataframe[column][i].item())
            if treshold_inf is not None:
                if dataframe[column][i] < treshold_inf:
                    outliers_inf.append(dataframe[column][i].item())

        if len(outliers_sup) > 0 and len(outliers_inf) > 0:
            logging.info(f"Found {len(outliers_sup)} upper outliers and {len(outliers_inf)} lower outliers")
            return outliers_sup, outliers_inf
        elif len(outliers_sup) > 0:
            logging.info(f"Found {len(outliers_sup)} upper outliers")
            return outliers_sup
        elif len(outliers_inf) > 0:
            logging.info(f"Found {len(outliers_inf)} lower outliers")
            return outliers_inf
        else:
            logging.info("There are no outliers for this column and this threshold")
            return []

def date_separated(col_name, dataframe):
    """
    This function takes a column with a date in the string format YYYY-MM-DD and returns 
    the dataframe with 3 new columns for the day, month, and year.

    Args:
        col_name (string): Name of the column with the date in the dataframe.
        dataframe : pandas.DataFrame

    Returns:
        dataframe : DataFrame with additional columns for day, month, and year.
    """
    logging.info("Running date_separated function")
    logging.debug(f"Arguments: col_name={col_name}")

    try:
        df = dataframe.copy()
        df[col_name] = pd.to_datetime(df[col_name])

        df['day'] = df[col_name].dt.day
        df['month'] = df[col_name].dt.month
        df['year'] = df[col_name].dt.year

        logging.info("Successfully added day, month, and year columns")
        return df

    except Exception as e:
        logging.error(f"Error in date_separated: {e}")
        raise

def add_season(df):
    """ Add a season column to the dataset """
    logging.info("Running add_season function")

    def get_season(month):
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        elif month in [9, 10, 11]:
            return 'autumn'

    try:
        df['season'] = df['month'].map(get_season)
        logging.info("Successfully added season column")
        return df
    except Exception as e:
        logging.error(f"Error in add_season: {e}")
        raise

def remove_outliers_iqr(df, column):
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    inter = q3 - q1
    lower_bound = q1 - 1.5 * inter
    upper_bound = q3 + 1.5 * inter
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

