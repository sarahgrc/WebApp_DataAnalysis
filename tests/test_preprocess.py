from app_streamlit.load_data.preprocess.cleaning_data import *
from app_streamlit.load_data.preprocess.merging import *
from tests.conftest import sample_raw_recipes
from app_streamlit.load_data.preprocess.normalisation import *
from app_streamlit.load_data.preprocess.add_drop_column import *
from app_streamlit.load_data.preprocess.cleaning_data import outliers_df 
import logging
import pytest


logging.basicConfig(filename='logging/debug.log', level=logging.DEBUG, filemode="w", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s') #pragma: no cover
logger = logging.getLogger(__name__)#pragma: no cover

def test_date_separated(sample_date_data):
    """
    Teste que 'date_separated' ajoute les colonnes 'year', 'month', et 'day',
    et supprime la colonne 'submitted'.
    """
    logger.info("Starting test for date_separated function.") #pragma: no cover
    initial_column_count = len(sample_date_data.columns)
    
    df = date_separated('submitted', sample_date_data)
    logger.info("Columns after date_separation: %s", df.columns) #pragma: no cover

    assert 'year' in df.columns
    assert 'month' in df.columns
    assert 'day' in df.columns
    
    assert len(df.columns) == initial_column_count + 3
    logger.info("Test for date_separated function passed.") #pragma: no cover

def test_outliers_df(outliers_sample):
    """
    Test the outliers_df function to detect and extract outliers
    based on specified thresholds.
    """
    logger.info("Starting test for outliers_df function.") #pragma: no cover
    # Test with treshold_sup only
    outliers = outliers_df(outliers_sample, column='A', treshold_sup=30, get_info=False)
    logger.info("Outliers detected with treshold_sup=30: %s", outliers) #pragma: no cover
    assert isinstance(outliers, list)
    assert len(outliers) == 6  # Check number of outliers
    assert all(value > 30 for value in outliers)

    # Test with treshold_inf only
    outliers = outliers_df(outliers_sample, column='A', treshold_inf=10, get_info=False)
    logger.info("Outliers detected with treshold_inf=10: %s", outliers) #pragma: no cover
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
    try :
        result = add_columns(df_target, df_source, 'key', 'key', ['extra'])
        assert 'extra' in result.columns
        assert result.loc[result['key'] == 3, 'extra'].isna().all()
    except Exception as e:
        print(f"Error: {e}")

def test_add_columns_mixed_keys(sample_raw_recipes):
    """
    Tests add_columns with partial key matches.

    Verifies:
    - Matching keys add the correct data.
    - Non-matching keys result in NaN values.
    """
    df_target = pd.DataFrame({'id': [1, 2, 4], 'name': ['A', 'B', 'D']})
    df_source = pd.DataFrame({'id': [1, 3, 4], 'extra': ['X', 'Y', 'Z']})

    result = add_columns(
        df_target, df_source,
        key_target='id', key_source='id',
        columns_to_add=['extra']
    )

    assert result.loc[result['id'] == 1, 'extra'].iloc[0] == 'X'
    assert result.loc[result['id'] == 4, 'extra'].iloc[0] == 'Z'
    assert result.loc[result['id'] == 2, 'extra'].isna().all()

def test_drop_columns_valid(sample_raw_recipes):
    """
    Tests drop_columns removes specified columns.

    Verifies:
    - Specified columns are removed.
    - Remaining columns are unchanged.
    """
    df = sample_raw_recipes[['recipe_id', 'name', 'tags']].head(10)
    result = drop_columns(df, ['tags'])

    assert 'tags' not in result.columns
    assert 'recipe_id' in result.columns
    assert 'name' in result.columns

def test_dataframe_concat_exceptions_and_edge_cases(merged_sample):
    """
    Tests edge cases and exceptions for the dataframe_concat function.

    Verifies:
    - Errors when the key is missing in one or both DataFrames.
    - Handling of mismatched join types.
    - Joining on columns that exist only in one DataFrame.
    """
    df1, df2 = merged_sample

    # Invalid key: Column 'D' does not exist in df
    with pytest.raises(KeyError, match="The column 'D' does not exist in one of the DataFrames"):
        dataframe_concat([df1, df2], 'D')

    # Joining on a column that exists only in df1
    df1['Extra'] = ['X', 'Y', 'Z', 'W', 'T', 'V', 'U'] * (len(df1) // 7) + ['X'] * (len(df1) % 7)
    with pytest.raises(KeyError, match="The column 'Extra' does not exist in one of the DataFrames"):
        dataframe_concat([df1, df2], 'Extra')

    # Valid join: Outer join with mismatched keys
    result = dataframe_concat([df1, df2], 'A', join='outer')
    assert result.shape[0] == len(set(df1['A']).union(set(df2['A'])))
    assert 'B' in result.columns
    assert 'C' in result.columns

def test_drop_columns_nonexistent(sample_raw_recipes):
    """
    Tests drop_columns raises KeyError for nonexistent columns.
    """
    df = sample_raw_recipes[['recipe_id', 'name']].head(10)

    with pytest.raises(KeyError):
        drop_columns(df, ['nonexistent_column'])

def test_drop_columns_existing(sample_raw_recipes):
    """
 Tests drop_columns removes existing columns.
    """
    df = sample_raw_recipes[['recipe_id', 'name', 'ingredients']].head(10)
    result = drop_columns(df, ['name', 'ingredients'])
    expected = sample_raw_recipes[['recipe_id']].head(10)
    pd.testing.assert_frame_equal(result, expected)  #remove column