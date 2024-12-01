from code.analyse.utils import *

def test_count_contributors_by_recipe_range_with_bins(sample_data):
    """Test the distribution of contributors based on the number of recipes contributed.

    Args:
        sample_data (DataFrame): A sample dataset containing recipe information.

    Asserts:
        - The count of contributors who contributed exactly 1 recipe is 3.
        - The count of contributors who contributed between 2 and 5 recipes is 3.
    """
    result = count_contributors_by_recipe_range_with_bins(sample_data)
    assert result['1 recette'] == 3
    assert result['2 à 5 recettes'] == 3

def test_top_contributors_by_recipes(sample_data):
    """Test retrieving the top contributors based on the number of recipes.

    Args:
        sample_data (DataFrame): A sample dataset containing recipe information.

    Asserts:
        - The result is not None.
        - The length of the result is 3 (top 3 contributors).
    """
    result = top_contributors_by_recipes(sample_data, top_n=3)
    assert result is not None
    assert len(result) == 3


def test_top_contributors_by_commented_recipes(sample_data):
    """Test retrieving the top contributors based on the number of commented recipes.

    Args:
        sample_data (DataFrame): A sample dataset containing recipe and comment information.

    Asserts:
        - The length of the result is 2 (top 2 contributors).
        - The first contributor in the result has an expected comment count of 2.
    """
    result = top_contributors_by_commented_recipes(sample_data, top_n=2)
    assert len(result) == 2
    assert result.iloc[0] == 2


def test_top_tags_recipes(sample_data):
    """Test retrieving the most common tags from recipes.

    Args:
        sample_data (DataFrame): A sample dataset containing recipe information, including tags.

    Asserts:
        - The length of the result is 2 (top 2 tags).
        - The tag 'vegan' is included in the result index.
    """
    result = top_tags(sample_data, top_n=2)
    assert len(result) == 2
    assert 'vegan' in result.index


def test_top_tags_most_commented(sample_data):
    """Test retrieving the most commented tags from the top recipes.

    Args:
        sample_data (DataFrame): A sample dataset containing recipe and comment information.

    Asserts:
        - The length of the result is 2 (top 2 tags).
        - The tag 'easy' is included in the result index.
        - The tag 'vegan' is included in the result index.
    """
    result = top_tags_most_commented(sample_data, top_recipes=5, top_n=2)
    assert len(result) == 2
    assert 'easy' in result.index  # Adjust expected values based on data
    assert 'vegan' in result.index


def test_get_top_ingredients(sample_data, ingredient_mapping):
    """Test retrieving the top ingredients from recipes.

    Args:
        sample_data (DataFrame): A sample dataset containing recipe information, including ingredients.
        ingredient_mapping (dict): A dictionary mapping raw ingredient names to standardized names.

    Asserts:
        - The length of the result is 3 (top 3 ingredients).
        - The ingredient 'onion' is included in the result index.
    """
    result = get_top_ingredients(sample_data, ingredient_mapping, excluded_ingredients={'salt'}, top_n=3)
    assert len(result) == 3
    assert 'onion' in result.index
