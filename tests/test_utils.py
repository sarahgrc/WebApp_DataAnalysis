import pytest
import pandas as pd
from app_streamlit.analyse.utils import *

def test_metrics_main_contributor(sample_raw_recipes):
    """
    Test that metrics_main_contributor returns the correct number of unique contributors and recipes.
    """
    result = metrics_main_contributor(sample_raw_recipes)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] > 0  # There should be at least one contributor
    assert result[1] > 0  # There should be at least one recipe

def test_average_and_total_comments_per_contributor(sample_raw_recipes):
    """
    Test that the average and total comments per contributor are calculated correctly.
    """
    result = average_and_total_comments_per_contributor(sample_raw_recipes)
    assert isinstance(result, pd.DataFrame)
    assert 'avg_comments_per_recipe' in result.columns
    assert 'total_comments' in result.columns
    assert result['avg_comments_per_recipe'].dtype == float
    assert result['total_comments'].dtype == int

def test_top_commented_recipes_by_contributors(sample_raw_recipes):
    """
    Test that the top commented recipes are correctly extracted for top contributors.
    """
    top_contributors = sample_raw_recipes[['contributor_id']].drop_duplicates().head(5)
    result = top_commented_recipes_by_contributors(sample_raw_recipes, top_contributors)
    assert isinstance(result, pd.DataFrame)
    assert 'recipe_id' in result.columns
    assert 'num_comments' in result.columns
    assert result['num_comments'].max() > 0  # There should be comments

def test_count_contributors_by_recipe_range_with_bins(sample_raw_recipes):
    """
    Test that contributors are correctly categorized into recipe count bins.
    """
    result = count_contributors_by_recipe_range_with_bins(sample_raw_recipes)
    assert isinstance(result, pd.Series)
    assert all(isinstance(label, str) for label in result.index)
    assert result.sum() > 0  # At least one contributor should fall into a bin

def test_top_commented_recipes(sample_raw_recipes):
    """
    Test that the top N commented recipes are correctly extracted.
    """
    result = top_commented_recipes(sample_raw_recipes, top_n=5)
    assert isinstance(result, pd.DataFrame)
    assert len(result) <= 5
    assert 'recipe_id' in result.columns
    assert 'num_comments' in result.columns
    assert result['num_comments'].iloc[0] >= result['num_comments'].iloc[-1]  # Sorted order

def test_get_top_tags(sample_raw_recipes):
    """
    Test that the top N tags are correctly extracted from the dataset.
    """
    sample_raw_recipes['tags'] = sample_raw_recipes['tags'].fillna("[]")  # Ensure no NaN values
    result = get_top_tags(sample_raw_recipes, most_commented=True, top_recipes=10, top_n=5)
    assert isinstance(result, pd.Series)
    assert len(result) <= 5
    assert all(isinstance(tag, str) for tag in result.index)

def test_get_top_ingredients2(sample_raw_recipes):
    """
    Test that the top ingredients are correctly extracted, excluding specified ingredients.
    """
    df_ingr_map = pd.DataFrame({'id': [1, 2, 3], 'replaced': ['salt', 'sugar', 'butter']})
    sample_raw_recipes['ingredient_ids'] = sample_raw_recipes['ingredient_ids'].fillna("[]")
    result = get_top_ingredients2(sample_raw_recipes, df_ingr_map, excluded_ingredients={'salt'}, top_n=5)
    assert isinstance(result, pd.Series)
    assert len(result) <= 5
    assert all(isinstance(ingredient, str) for ingredient in result.index)
    assert 'salt' not in result.index