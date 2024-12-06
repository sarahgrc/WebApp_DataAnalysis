from app_streamlit.analyse.utils import *


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

def test_user_recipes(recipes_table):
    # Get recipes for the specific user
    user_recipes_df = user_recipes(recipes_table, 47892)

    # Check the 'name' column contains the correct recipe names
    assert list(user_recipes_df['name']) == ["Recipe1", "Recipe2"]  # Ensure names match exactly


# Test for the top_recipes_user function
def test_top_recipes_user(top_recipes_data):
    user_id = 1  # User to test
    
    # Call the top_recipes_user function with the sample DataFrame
    top_results_by_user = top_recipes_user(top_recipes_data)
    
    # Check the structure of the output
    assert isinstance(top_results_by_user, pd.DataFrame), "The result should be a DataFrame"
    assert 'Recipe' in top_results_by_user.columns, "The DataFrame should contain a 'Recipe' column"
    assert 'Number of comments' in top_results_by_user.columns, "The DataFrame should contain a 'Number of comments' column"
    
    # Check that the returned recipes are correct"
    assert top_results_by_user.iloc[0]['Recipe'] == 'Recipe A', "The first recipe should be 'Recipe A'"
    assert top_results_by_user.iloc[1]['Recipe'] == 'Recipe B', "The second recipe should be 'Recipe B'"
    
    # Check the number of comments
    assert top_results_by_user.iloc[0]['Number of comments'] == 3, "Recipe A should have 3 comments"
    
    # Check if the function returns at most the top 5 recipes (even though here we have less)
    assert top_results_by_user.shape[0] <= 5, "There should not be more than 5 recipes returned"

    top_results = top_recipes(top_recipes_data)

    # Check the structure of the output
    assert isinstance(top_results, pd.DataFrame), "The result should be a DataFrame"
    assert 'Recipe' in top_results.columns, "The DataFrame should contain a 'Recipe' column"
    assert 'Number of comments' in top_results.columns, "The DataFrame should contain a 'Number of comments' column"
    assert 'Mean Rating' in top_results.columns, "The DataFrame should contain a 'Mean Rating' column"

    # Check that the returned recipes are correct"
    assert top_results.iloc[0]['Recipe'] == 'Recipe A', "The first recipe should be 'Recipe A'"
    assert top_results.iloc[1]['Recipe'] == 'Recipe B', "The second recipe should be 'Recipe B'"

    # Check the number of comments
    assert top_results.iloc[0]['Number of comments'] == 3, "Recipe A should have 3 comments" 

    # Check if the function returns at most the top 5 recipes (even though here we have less)
    assert top_results.shape[0] <= 5, "There should not be more than 5 recipes returned"

def test_nutri_score(nutriments_data):
    assert nutri_score(nutriments_data) == "A"
