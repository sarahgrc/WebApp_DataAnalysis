import pytest
import pandas as pd
from app_streamlit.analyse.utils import * 
from unittest.mock import patch
from app_streamlit.analyse.utils import nutri_score

def test_metrics_main_contributor(sample_raw_recipes):
    """
    Test that metrics_main_contributor returns the correct number of unique contributors and recipes.
    """
    result = metrics_main_contributor(sample_raw_recipes)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] > 0  # at least one contributor
    assert result[1] > 0  # at least one recipe

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
    assert result['num_comments'].max() > 0  

def test_count_contributors_by_recipe_range_with_bins(sample_raw_recipes):
    """
    Test that contributors are correctly categorized into recipe count bins.
    """
    result = count_contributors_by_recipe_range_with_bins(sample_raw_recipes)
    assert isinstance(result, pd.Series)
    assert all(isinstance(label, str) for label in result.index)
    assert result.sum() > 0  

def test_top_commented_recipes(sample_raw_recipes):
    """
    Test that the top N commented recipes are correctly extracted.
    """
    result = top_commented_recipes(sample_raw_recipes, top_n=5)
    assert isinstance(result, pd.DataFrame)
    assert len(result) <= 5
    assert 'recipe_id' in result.columns
    assert 'num_comments' in result.columns
    assert result['num_comments'].iloc[0] >= result['num_comments'].iloc[-1] 

def test_get_top_tags(sample_raw_recipes):
    """
    Test that the top N tags are correctly extracted from the dataset.
    """
    sample_raw_recipes['tags'] = sample_raw_recipes['tags'].fillna("[]") 
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

def test_user_recipes(recipes_table):
    # Get recipes for the specific user
    user_recipes_df = user_recipes(recipes_table, 47892)

    # Check the 'name' column contains the correct recipe names
    assert list(user_recipes_df['name']) == ["Recipe1", "Recipe2"]  # Ensure names match exactly


# Test for the top_recipes_user function
def test_top_recipes_user(sample_raw_recipes):
    """
    Test the `top_recipes_user` function with the sample_raw_recipes dataset.
    """
    # Appeler la fonction avec le DataFrame sample_raw_recipes
    top_results_by_user = top_recipes_user(sample_raw_recipes)

    # Vérifiez que la sortie est un DataFrame
    assert isinstance(top_results_by_user, pd.DataFrame), "Le résultat doit être un DataFrame"
    assert 'Recipe' in top_results_by_user.columns, "Le DataFrame doit contenir une colonne 'Recipe'"
    assert 'Number of comments' in top_results_by_user.columns, "Le DataFrame doit contenir une colonne 'Number of comments'"
    assert 'Average Rating' in top_results_by_user.columns, "Le DataFrame doit contenir une colonne 'Average Rating'"

    # Vérifiez les résultats attendus
    assert top_results_by_user.shape[0] <= 5, "Il ne doit pas y avoir plus de 5 recettes dans le résultat"

    # Assurez-vous que les recettes sont triées correctement
    assert top_results_by_user['Number of comments'].is_monotonic_decreasing, \
        "Les résultats doivent être triés par nombre de commentaires décroissants"

def test_nutri_score(nutriments_data):
    assert nutri_score(nutriments_data) == "A"



# Sample function for getting top ingredients, as assumed to be working
def get_top_ingredients2(season_df, ingr_map, excluded_ingredients, top_n):
    # Return a mock series with fake ingredients based on the season
    return pd.Series([f'{season_df["season"].iloc[0]}_ingredient{n+1}' for n in range(top_n)])


# Test function using pytest
def test_trendy_ingredients_by_seasons():
    # Sample DataFrame with 'season' and 'ingredients' columns for the test
    df_sample = pd.DataFrame({
        'season': ['winter', 'spring', 'summer', 'autumn', 'winter', 'spring', 'summer', 'autumn'],
        'ingredients': ['ingredient1', 'ingredient2', 'ingredient3', 'ingredient4', 'ingredient5', 'ingredient6', 'ingredient7', 'ingredient8']
    })

    # Sample ingredient mapping (normally this would be a more detailed map)
    ingr_map_sample = pd.DataFrame({
        'id': [1, 2, 3, 4, 5, 6, 7, 8],
        'replaced': ['ingredient1', 'ingredient2', 'ingredient3', 'ingredient4', 'ingredient5', 'ingredient6', 'ingredient7', 'ingredient8']
    })

    top_n = 3  # We want the top 3 ingredients per season

    # Call the function we're testing
    winter_ingr, spring_ingr, summer_ingr, autumn_ingr = trendy_ingredients_by_seasons(df_sample, ingr_map_sample, top_n)

    # Assertions
    assert isinstance(winter_ingr, pd.Series), "Winter ingredients should be a Pandas Series"
    assert len(winter_ingr) == top_n, "Winter ingredients list should have 3 items"
    assert winter_ingr[0] == 'winter_ingredient1', "First winter ingredient should be 'winter_ingredient1'"

    assert isinstance(spring_ingr, pd.Series), "Spring ingredients should be a Pandas Series"
    assert len(spring_ingr) == top_n, "Spring ingredients list should have 3 items"
    assert spring_ingr[0] == 'spring_ingredient1', "First spring ingredient should be 'spring_ingredient1'"

    assert isinstance(summer_ingr, pd.Series), "Summer ingredients should be a Pandas Series"
    assert len(summer_ingr) == top_n, "Summer ingredients list should have 3 items"
    assert summer_ingr[0] == 'summer_ingredient1', "First summer ingredient should be 'summer_ingredient1'"

    assert isinstance(autumn_ingr, pd.Series), "Autumn ingredients should be a Pandas Series"
    assert len(autumn_ingr) == top_n, "Autumn ingredients list should have 3 items"
    assert autumn_ingr[0] == 'autumn_ingredient1', "First autumn ingredient should be 'autumn_ingredient1'"


def test_visualise_recipe_season(visu_data):
    """ Test visualise_recipe_season function"""
    fig = visualise_recipe_season(visu_data)
    assert isinstance(visu_data, pd.DataFrame), "L'entrée doit être un dataframe"
    assert isinstance(fig, plt.Figure), "La sortie doit être une figure Matplotlib"

    assert fig.axes[0].get_title() == "Recipes count per season", "Le titre du graphique est incorrect"
    assert fig.axes[0].get_xlabel() == "Season", "L'étiquette de l'axe X est incorrecte"
    assert fig.axes[0].get_ylabel() == "Count", "L'étiquette de l'axe Y est incorrecte"

    legend_labels = [text.get_text() for text in fig.axes[0].get_legend().get_texts()]
    assert "Low ranking" in legend_labels, "La légende doit contenir 'Low ranking'"
    assert "High ranking" in legend_labels, "La légende doit contenir 'High ranking'"

def test_visualise_low_rank_insight(df_low_count):
    """ Test the visualisation low rank function """
    df_l, df_h = test_visualise_low_rank_insight()
    fig = visualise_low_rank_insight(df_low_count)
    assert isinstance(df_low_count, pd.DataFrame)
    assert isinstance(fig, plt.Figure)
    assert fig.axes[0].get_title() == 'Sum of recipies (in %) per time of  preparation '
    assert fig.axes[0].get_xlabel() == 'time of preparation'
    assert fig.axes[0].get_ylabel() == '% of recipies'


def test_unique_ingr(sample_raw_recipes,ingr_map):
    assert isinstance(sample_raw_recipes, pd.DataFrame)
    df1,df2,df3,df4=unique_ingr(sample_raw_recipes,ingr_map,top_n=10)
    assert isinstance(df1,list)
    assert isinstance(df2,list)
    assert isinstance(df3,list)
    assert isinstance(df4,list)

def test_top_recipes_top_three(sample_date_avgrating):
    """
    Tests that top_recipes works correctly and returns the top 3 recipes when there are exactly 3 recipes.
    """
    # Reduce the data to three recipes
    test_data = sample_date_avgrating.iloc[:3]

    # Expected result
    expected_data = pd.DataFrame({
        'Recipe': ['Recipe B', 'Recipe A', 'Recipe C'],
        'Number of comments': [50, 10, 5],
        'Avg Rating': [3.8, 4.5, 4.7]
    })

    # Call the function and verify the result
    result = top_recipes(test_data)

    # Check that the output contains exactly 3 recipes sorted by the number of comments
    assert len(result) == 3, "The result should contain exactly 3 recipes."
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_data)

def test_assign_grade():
    # Test case for score <= -1
    assert nutri_score(-1) == "A"
    assert nutri_score(-2) == "A"
    assert nutri_score(-1000) == "A"

    # Test case for 0 <= score <= 2
    assert nutri_score(0) == "B"
    assert nutri_score(1) == "B"
    assert nutri_score(2) == "B"

    # Test case for 3 <= score <= 10
    assert nutri_score(3) == "C"
    assert nutri_score(5) == "C"
    assert nutri_score(10) == "C"

    # Test case for 11 <= score <= 18
    assert nutri_score(11) == "D"
    assert nutri_score(15) == "D"
    assert nutri_score(18) == "D"

    # Test case for score > 18
    assert nutri_score(19) == "E"
    assert nutri_score(25) == "E"
    assert nutri_score(1000) == "E"

    # Test case for floating point values
    assert nutri_score(1.5) == "B"
    assert nutri_score(7.5) == "C"
    assert nutri_score(16.2) == "D"
    assert nutri_score(20.7) == "E"

def test_visualise_recipe_season(sample_data):
        
    # Call the function with the sample data
    fig = visualise_recipe_season(sample_data)
    
    # Check that the plot is created (it should return a figure object)
    assert isinstance(fig, plt.Figure), "Returned object is not a matplotlib figure"
    
    # Check that the legend labels exist on the plot
    ax = fig.axes[0]  # Get the Axes object from the figure
    legend_labels = [text.get_text() for text in ax.get_legend().get_texts()]
    assert 'Low ranking' in legend_labels, "Low ranking label missing in legend"
    assert 'High ranking' in legend_labels, "High ranking label missing in legend"
    
    # Check that the correct bars are plotted
    # There should be 2 bars for each season, one for low-ranking and one for high-ranking
    assert len(ax.patches) == 6, "The number of bars in the plot is incorrect"
    
    # Check if the bars are color-coded correctly (low = blue, high = orange)
    low_bars = [patch for patch in ax.patches if patch.get_facecolor() == sns.color_palette("Blues")[0]]
    high_bars = [patch for patch in ax.patches if patch.get_facecolor() == sns.color_palette("Oranges")[1]]
    
    assert len(low_bars) == 3, "Incorrect number of low-ranking bars"
    assert len(high_bars) == 3, "Incorrect number of high-ranking bars"

def test_group_by_season_and_count(sample_data):
    """Test if the grouping by season and count calculation works correctly."""
    df_high = sample_data[sample_data['avg_ratings'].isin([4, 5])]
    df_low = sample_data[sample_data['avg_ratings'].isin([1, 2, 3])]

    count_data_high = df_high.groupby(['season']).size().reset_index(name='count')
    count_data_low = df_low.groupby(['season']).size().reset_index(name='count')

    # Verify correct groupings and counts
    assert count_data_high.loc[count_data_high['season'] == 'Summer', 'count'].iloc[0] == 2, "High-ranking count for Summer is incorrect"
    assert count_data_high.loc[count_data_high['season'] == 'Winter', 'count'].iloc[0] == 1, "High-ranking count for Winter is incorrect"
    assert count_data_low.loc[count_data_low['season'] == 'Winter', 'count'].iloc[0] == 1, "Low-ranking count for Winter is incorrect"
    assert count_data_low.loc[count_data_low['season'] == 'Fall', 'count'].iloc[0] == 2, "Low-ranking count for Fall is incorrect"

