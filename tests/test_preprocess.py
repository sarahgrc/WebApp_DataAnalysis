from app_streamlit.load_data.preprocess.cleaning_data import *
from app_streamlit.load_data.preprocess.merging import *
from tests.conftest import sample_raw_recipes
from app_streamlit.load_data.preprocess.normalisation import *
from app_streamlit.load_data.preprocess.add_drop_column import *


def test_date_separated(sample_raw_recipes):
    """
    Tests the 'date_separated' function on a sample DataFrame.

    Verifies that the specific columns ('year', 'month', 'day') are
    correctly added to the input DataFrame, without removing any existing
    columns or rows.

    Args:
    sample_raw_recipes (pd.DataFrame): A DataFrame containing the raw
    data, including a `submitted` column that will be separated into
    'year', 'month', and 'day'.
    """
    assert len(
        sample_raw_recipes.columns) == 13  # Check th initial number of columns
    d = date_separated('submitted', sample_raw_recipes)

    # Checks that columns `year`, `month`, and `day` have been added
    assert ('year' in d.columns)
    assert ('month' in d.columns)
    assert ('day' in d.columns)

    # Checks no lines bhave been removed
    assert len(d) == 200

    # Checks no columns bhave been removed  and 3 columns have been added
    assert len(d.columns) == len(sample_raw_recipes.columns) + 3


def test_outliers(outliers_sample):
    """
    Tests the 'outliers' function to detect and extract outliers
    in a sample DataFrame.

    Verifies that outlier detection works above and below
    the given thresholds, and that information is returned in the requested mode.

    Args:
    outliers_sample (DataFrame): A DataFrame containing numeric columns
    used to test outlier detection.
    """
    # Tests values above a given treshold
    outlier = outliers(outliers_sample, 'A', treshold_sup=30,
                       treshold_inf=None, get_info=False)
    assert isinstance(outlier, list)  # Check result is a list
    assert len(outlier) == 6  # Check the amount of values above the treshold

    # Tests values below a given treshold
    outlier1 = outliers(outliers_sample, 'A', treshold_sup=None,
                        treshold_inf=10, get_info=False)
    assert isinstance(outlier1, list)
    assert len(outlier1) == 4

    # Tests values between two tresholds and returns info
    outlier2 = outliers(outliers_sample, 'A', treshold_sup=16,
                        treshold_inf=37, get_info=True)
    assert isinstance(outlier2, pd.DataFrame)  # Check result is a dataframe
    assert len(outlier2) == 7  # check values are correctly filtered


def test_df_merged(merged_sample):
    """
    Test the 'dataframe_concat' function for merging DataFrames.

    Checks that each join type ('left', 'right', 'outer', 'inner')
    returns a DataFrame with the correct size.

    Args:
    merged_sample (tuple): A tuple containing two DataFrames, sharing
    a common column `A` and specific columns ('B' or 'C'),
    to test different merge configurations.
    """
    df = [merged_sample[0], merged_sample[1]]

    # Check each fixture returns the correct number of columns
    type_join = ["left", "right", "outer", "inner"]
    for i in type_join:
        merging = dataframe_concat(df, 'A', join=i)
        assert len(merging.columns) == 3


def test_normalisation(normalisation_data):
    """
    Tests the `normalisation` function to ensure it correctly normalizes 
    a numeric column in a DataFrame.

    The test checks that:
    - The normalized column is added to the DataFrame with the expected name.
    - The minimum value in the normalized column is 0.
    - The maximum value in the normalized column is 1.

    Args:
        normalisation_data (pd.DataFrame): A fixture providing a sample DataFrame 
                                           with a single numeric column.
    """
    result = normalisation(normalisation_data, 'value')
    assert 'value_normalisé' in result.columns
    assert result['value_normalisé'].iloc[0] == 0
    assert result['value_normalisé'].iloc[-1] == 1


def test_add_columns(column_merge_data):
    """
    Tests the `add_columns` function to ensure it correctly merges additional 
    columns from a source DataFrame into a target DataFrame based on a common key.

    The test verifies that:
    - The new column is successfully added to the target DataFrame.
    - Missing keys in the source DataFrame result in NaN values in the merged column.

    Args:
        column_merge_data (tuple): A fixture providing two DataFrames:
                                   - Target DataFrame with keys and values.
                                   - Source DataFrame with keys and additional columns to merge.
    """
    df_target, df_source = column_merge_data
    result = add_columns(df_target, df_source, 'key', 'key', ['extra'])
    assert 'extra' in result.columns
    assert result.loc[result['key'] == 3, 'extra'].isna().all()
