from app_streamlit.load_data.preprocess.cleaning_data import *
from app_streamlit.load_data.preprocess.merging import *
from tests.conftest import sample_raw_recipes
from app_streamlit.load_data.preprocess.normalisation import *
from app_streamlit.load_data.preprocess.add_drop_column import *
from app_streamlit.load_data.preprocess.cleaning_data import outliers_df 

def test_date_separated(sample_date_data):
    """
    Teste que 'date_separated' ajoute les colonnes 'year', 'month', et 'day',
    et supprime la colonne 'submitted'.
    """
    initial_column_count = len(sample_date_data.columns)
    
    df = date_separated('submitted', sample_date_data)
    
    assert 'year' in df.columns
    assert 'month' in df.columns
    assert 'day' in df.columns
    
    assert len(df.columns) == initial_column_count + 3


def test_outliers_df(outliers_sample):
    """
    Test the outliers_df function to detect and extract outliers
    based on specified thresholds.
    """
    # Test with treshold_sup only
    outliers = outliers_df(outliers_sample, column='A', treshold_sup=30, get_info=False)
    assert isinstance(outliers, list)
    assert len(outliers) == 6  # Check number of outliers
    assert all(value > 30 for value in outliers)

    # Test with treshold_inf only
    outliers = outliers_df(outliers_sample, column='A', treshold_inf=10, get_info=False)
    assert isinstance(outliers, list)
    assert len(outliers) == 4  # Check number of outliers
    assert all(value < 10 for value in outliers)

    # Test with both treshold_sup and treshold_inf
    outliers_info = outliers_df(outliers_sample, column='A', treshold_sup=10, treshold_inf=30, get_info=True)
    assert isinstance(outliers_info, pd.DataFrame)
    assert len(outliers_info) == 6  # Check filtered rows
    assert all(outliers_info['A'].between(10, 30, inclusive='neither'))



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
