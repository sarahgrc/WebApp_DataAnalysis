"""
Module de tests pour l'analyse de données.

Ce fichier contient des tests unitaires et des fixtures utilisées avec pytest 
pour tester les fonctionnalités d'analyse, de nettoyage et de manipulation 
de données. Les tests couvrent plusieurs cas, comme le nettoyage des données, 
la gestion des valeurs aberrantes, et la fusion de DataFrames.
"""

import pandas as pd
import numpy as np
import pytest

@pytest.fixture
def sample_raw_recipes():
    """
    Fixture qui charge un échantillon de données brutes de recettes.

    Ce DataFrame contient les colonnes nécessaires pour tester les 
    transformations de données telles que la séparation de colonnes 
    et l'ajout de nouvelles informations temporelles.

    Returns:
        pd.DataFrame: Un DataFrame contenant les données brutes de recettes.
    """
    df = pd.read_csv('sample/sample_raw_recipes.csv')
    return df

@pytest.fixture
def outliers_sample():
    """
    Fixture qui génère un échantillon de données pour tester 
    la gestion des valeurs aberrantes.

    Le DataFrame généré contient deux colonnes numériques avec 
    des valeurs incrémentales permettant de simuler différentes
    plages de données.

    Returns:
        pd.DataFrame: Un DataFrame contenant deux colonnes `A` et `B` 
        avec des valeurs incrémentales.
    """
    df = pd.DataFrame({'A': np.arange(0, 50, 3), 'B': np.arange(20, 70, 3)})
    return df

@pytest.fixture
def merged_sample():
    """
    Fixture qui génère deux DataFrames pour tester la fusion.

    Ces DataFrames contiennent des colonnes communes et différentes, 
    permettant de valider les opérations de jointure sous plusieurs 
    configurations (`left`, `right`, `inner`, `outer`).

    Returns:
        tuple: Deux DataFrames avec une colonne commune `A` et une colonne 
        spécifique (`B` ou `C`).
    """
    df1 = pd.DataFrame({'A': np.arange(0, 50, 3), 'B': np.arange(20, 70, 3)})
    df2 = pd.DataFrame({'A': np.arange(0, 50, 3), 'C': np.arange(100, 150, 3)})
    return df1, df2

@pytest.fixture

def sample_data():
    """
    Provides sample data for testing functions in the utilzs module.

    This data simulates a recipe dataset with contributors, recipes, tags, reviews, 
    and ingredient IDs to support testing of various functionalities.

    Returns:
        pd.DataFrame: A DataFrame containing sample data with the following columns:
            - 'contributor_id' (int): IDs of contributors who created the recipes.
            - 'recipe_id' (int): Unique IDs of the recipes.
            - 'tags' (str): Tags associated with each recipe in JSON-like string format.
            - 'review' (str): Reviews or comments on the recipes (can be None).
            - 'ingredient_ids' (str): IDs of ingredients used in each recipe in JSON-like string format.
    """
    data = {
        'contributor_id': [1, 2, 1, 3, 2, 4, 5, 5, 5, 6],
        'recipe_id': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
        'tags': ['["vegan", "healthy"]', '["quick", "easy"]', '["vegan"]',
                 '["healthy", "low-fat"]', '["easy"]', '["quick"]',
                 '["vegan", "gluten-free"]', '["healthy"]', '["low-fat"]', '["quick"]'],
        'review': [None, 'Great recipe!', 'Loved it!', None, 'Too salty', None, 'Perfect!', 'Not bad', None, 'Amazing'],
        'ingredient_ids': ['[1, 2, 3]', '[4, 5]', '[1, 3]', '[6]', '[2, 7]', '[8]', '[9]', '[10]', '[11]', '[12]']
    }
    return pd.DataFrame(data)


@pytest.fixture
def ingredient_mapping():   
    """
    Provides a sample DataFrame for ingredient mapping.

    This fixture returns a mapping of ingredient IDs to their corresponding 
    simplified names, which can be used for testing ingredient-related functions.

    Returns:
        pd.DataFrame: A DataFrame with the following columns:
            - 'id' (int): Unique IDs representing individual ingredients.
            - 'replaced' (str): Simplified names of the corresponding ingredients.
    """
    data = {
        'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'replaced': [
            'onion', 'garlic', 'pepper', 'tomato', 'salt', 'olive oil', 'butter',
            'flour', 'sugar', 'milk', 'egg', 'yeast'
        ]
    }
    return pd.DataFrame(data)

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
