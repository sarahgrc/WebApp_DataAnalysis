"""
This file contains unit tests and fixtures used with pytest
to test data analysis, cleaning, and manipulation features. The tests cover several cases, such as data cleaning,
outlier handling, and merging DataFrames. 
"""

import pandas as pd
import numpy as np
import pytest


@pytest.fixture
def sample_raw_recipes():
    """
    Fixture that loads a sample of raw recipe data.

    This DataFrame contains the columns needed to test
    data transformations such as splitting columns
    and adding new time information.

    Returns:
    df (DataFrame): A DataFrame containing the raw recipe data.
    """
    df = pd.read_csv('sample/sample_raw_recipes.csv')
    return df

@pytest.fixture
def outliers_sample():
    """
    Fixture that generates a sample of data to test
    outlier handling.

    The generated DataFrame contains two numeric columns with
    incremental values to simulate different data ranges.

    Returns:
    df (DataFrame): A DataFrame containing two columns 'A' and 'B'
    with incremental values.
    """
    df = pd.DataFrame({'A': np.arange(0, 50, 3), 'B': np.arange(20, 70, 3)})
    return df

@pytest.fixture
def merged_sample():
    """
    Fixture that generates two DataFrames to test the merge.

    These DataFrames contain common and different columns,
    allowing to validate join operations under several configurations ('left', 'right', 'inner', 'outer').

    Returns:
    tuple: Two DataFrames with a common column 'A' and a specific column
    ('B' or 'C').
    """
    df1 = pd.DataFrame({'A': np.arange(0, 50, 3), 'B': np.arange(20, 70, 3)})
    df2 = pd.DataFrame({'A': np.arange(0, 50, 3), 'C': np.arange(100, 150, 3)})
    return df1, df2

@pytest.fixture
def normalisation_data():
    """
    Provides a sample DataFrame for testing the `normalisation` function.

    This fixture creates a DataFrame with a single numeric column to validate 
    the normalization process.

    Returns:
        pd.DataFrame: A DataFrame with the following column:
            - 'value' (int): A numeric column with sample values to normalize.
    """
    return pd.DataFrame({'value': [10, 20, 30]})

@pytest.fixture
def column_merge_data():
    """
    Provides sample DataFrames for testing the `add_columns` function.

    This fixture creates two DataFrames:
    - A target DataFrame with keys and values.
    - A source DataFrame with keys and additional columns to merge.

    Returns:
        tuple: A tuple containing:
            - df_target (pd.DataFrame): The target DataFrame with the following columns:
                - 'key' (int): Keys for merging.
                - 'value' (str): Values associated with each key.
            - df_source (pd.DataFrame): The source DataFrame with the following columns:
                - 'key' (int): Keys for merging.
                - 'extra' (str): Additional column to merge with the target DataFrame.
    """
    df_target = pd.DataFrame({'key': [1, 2, 3], 'value': ['A', 'B', 'C']})
    df_source = pd.DataFrame({'key': [1, 2, 4], 'extra': ['X', 'Y', 'Z']})
    return df_target, df_source


@pytest.fixture
def recipes_table():
    """
    Provides a sample DataFrame for testing recipe data by user.

    This fixture creates a DataFrame with recipe data that includes:
    - contributor_id
    - name: name of the recipe.
    - rating: rating given to each recipe.

    Args:  
        None

    Returns:
        pd.DataFrame: A DataFrame containing recipe data with the following columns:
            - 'contributor_id' (int)
            - 'name' (str)
            - 'rating' (int)
    """
    data = pd.DataFrame({
        'contributor_id': [47892, 47892, 12345],  # Contributor IDs
        'name': ['Recipe1', 'Recipe2', 'Recipe1'],  # Recipe names
        'rating': [5, 4, 3]  # Ratings for each recipe
    })
    return data

@pytest.fixture
def nutriments_data():
    """
    Provides a sample of a row of a DataFrame for testing the calcul of the nutri-socre

    This fixture creates a dictionnary representing the nutrients of 1 recipe
    - Calories 
    - Sugar 
    - Saturated Fat
    - Sodium
    - Protein

    Args:  
        None

    Returns:
        A Dictionnary containing the nutrients of 1 recipe.
            - "Calories" (float)
            - "Sugar" (float)
            - "Saturated_Fat" (float)
            - "Sodium" (flaoa)
            - "Protein" (float)
    """
    data = {
        'Calories': 335.0, 
        'Sugar': 4.5, 
        'Saturated Fat': 1.0, 
        'Sodium': 90.0, 
        'Protein': 10.0 
    }
    return data

@pytest.fixture
def outliers_sample():
    """
    Fixture that generates a sample of data to test
    outlier handling.

    The generated DataFrame contains two numeric columns with
    incremental values to simulate different data ranges.

    Returns:
    df (DataFrame): A DataFrame containing two columns 'A' and 'B'
    with incremental values.
    """
    df = pd.DataFrame({'A': np.arange(0, 50, 3), 'B': np.arange(20, 70, 3)})
    return df

@pytest.fixture
def sample_date_data():
    """
    Fixture qui crée un DataFrame contenant une colonne 'submitted' avec des dates pour tester la fonction 'date_separated'.
    """
    data = {
        'recipe_id': [1, 2, 3, 4, 5],
        'name': ['Recipe A', 'Recipe B', 'Recipe C', 'Recipe D', 'Recipe E'],
        'submitted': ['2023-01-01', '2023-02-15', '2023-03-20', '2023-04-10', '2023-05-05'],
    }
    return pd.DataFrame(data)

@pytest.fixture
def visu_data():
    """ Fixture to test the visualisation season function"""
    data = {
        'avg_ratings': [5, 4, 3, 2, 1, 5, 4],
        'season': ['Winter', 'Winter', 'Spring', 'Spring', 'Summer', 'Summer', 'Autumn']
    }
    df = pd.DataFrame(data)
    return df

@pytest.fixture
def df_low_count():
    # Données factices pour les tests
    df_low_count = pd.DataFrame({
        'minutes_tr': ['0-10', '10-20', '20-30'],
        'count': [10, 15, 5]
    })
    return df_low_count

@pytest.fixture
def df_high_count():
    df_high_count = pd.DataFrame({
        'minutes_tr': ['0-10', '10-20', '20-30'],
        'count': [5, 25, 10]
    })
    return df_high_count

@pytest.fixture
def ingr_map():
    return pd.read_pickle('data_files/ingr_map.pkl')

@pytest.fixture
def sample_date_avgrating():
    """summary
    """
    test_data = pd.DataFrame({
        'name': ['Recipe A', 'Recipe B', 'Recipe C', 'Recipe D', 'Recipe E', 'Recipe F'],
        'num_comments': [10, 50, 5, 0, 30, 20],
        'avg_ratings': [4.5, 3.8, 4.7, 4.2, 4.0, 3.5]
    })