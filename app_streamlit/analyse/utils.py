"""Function used for statistics. 
"""
import ast
import pandas as pd

from .classification_values import main_values



def count_contributors_by_recipe_range_with_bins(df):
    """
    Categorizes contributors based on the number of unique recipes they have contributed 
    and counts how many contributors fall into each category.

    Parameters:
    - df (pd.DataFrame): A DataFrame containing at least two columns: 
        'contributor_id' (unique identifier for contributors) 
        'recipe_id' (unique identifier for recipes).

    Returns:
    - pd.Series: A series where the index represents the recipe range categories 
      and the values are the counts of contributors in each category.

    The recipe ranges (bins) and their corresponding labels:
    - '1 recipe': Contributors with exactly 1 unique recipe.
    - '2 to 5 recipes': Contributors with 2 to 5 unique recipes.
    - '6 to 8 recipes': Contributors with 6 to 8 unique recipes.
    - 'More than 8 recipes': Contributors with more than 8 unique recipes.
    """
    # Compter le nombre de recettes uniques par contributeur
    recipe_counts = df.groupby('contributor_id')['recipe_id'].nunique()

    # Définir les plages de recettes (bins)
    bins = [0, 1, 5, 8, float('inf')]
    labels = ['1 recette', '2 à 5 recettes',
              '6 à 8 recettes', 'Plus de 10 recettes']

    # Découper en catégories
    binned_counts = pd.cut(recipe_counts, bins=bins, labels=labels, right=True)

    # Compter le nombre de contributeurs dans chaque bin
    contributor_counts_by_bin = binned_counts.value_counts().sort_index()

    return contributor_counts_by_bin


def top_contributors_by_commented_recipes(df, top_n=10):
    """
    Returns the top X contributors who have published the most unique recipes.

    Parameters:
    - df (pd.DataFrame): A DataFrame containing recipe data.
    - top_n (int): Number of top contributors to return.

    Returns:
    - pd.Series: The `top_n` contributors with the count of unique recipes they have published.
    """
    # Filtrer les recettes qui ont des commentaires
    commented_recipes = df.dropna(subset=['review'])

    # Compter le nombre de commentaires par recette, puis par contributeur
    comments_per_contributor = commented_recipes.groupby(
        'contributor_id')['recipe_id'].count().sort_values(ascending=False).head(top_n)

    return comments_per_contributor


def top_tags(df, top_n=20):
    """
    Ensures each recipe_id is unique and returns the most frequently used tags.

    Parameters:
    - df (pd.DataFrame): A DataFrame containing recipe data.
    - top_n (int): Number of most frequent tags to return.

    Returns:
    - pd.Series: The `top_n` most frequently used tags.

    Raises:
    - ValueError: If duplicate `recipe_id` entries are detected.
    """

    # Exploser les tags pour avoir des lignes individuelles
    tags_series = df['tags'].apply(eval).explode()

    # Compter les tags les plus fréquents
    top_tags_used = tags_series.value_counts().head(top_n)
    return top_tags_used


def top_tags_most_commented(df, top_recipes=20, top_n=10):
    """
    Returns the most frequently used tags among the top X most commented recipes.

    Parameters:
    - df (pd.DataFrame): A DataFrame containing recipe data.
    - top_recipes (int): Number of most commented recipes to consider.
    - top_n (int): Number of most frequent tags to return.

    Returns:
    - pd.Series: The `top_n` most frequently used tags.
    """

    # Supprimer les recettes sans commentaires
    commented_recipes = df.dropna(subset=['review'])

    # Identifier les recettes les plus commentées
    most_commented = commented_recipes['recipe_id'].value_counts().head(
        top_recipes).index

    # Filtrer pour ces recettes
    filtered_df = df[df['recipe_id'].isin(most_commented)]

    # Exploser les tags et compter
    tags_series = filtered_df['tags'].apply(eval).explode()
    top_tags_commented = tags_series.value_counts().head(top_n)
    return top_tags_commented


def top_contributors_by_recipes(df, top_n=10):
    """
    Identifies the top contributors based on the number of unique recipes they have published.

    Args:
        df (pd.DataFrame): DataFrame containing recipe data with at least the following columns:
            - 'contributor_id': Unique identifier for contributors.
            - 'recipe_id': Unique identifier for recipes.
        top_n (int, optional): Number of top contributors to return. Defaults to 10.

    Returns:
        pd.Series: A series with the top `top_n` contributors as the index and the count of unique recipes 
                   they have published as the values, sorted in descending order. Returns None if required 
                   columns are missing.
    """
    if 'contributor_id' not in df or 'recipe_id' not in df:
        return None
    unique_recipes_df = df.drop_duplicates(subset='recipe_id')
    return unique_recipes_df['contributor_id'].value_counts().head(top_n)


def get_top_ingredients(merged_df, df_ingr_map, excluded_ingredients=None, top_n=10):
    """Finds the most frequently used ingredients, excluding common ones.

    Args:
        merged_df (pd.DataFrame): DataFrame with recipe data, including 'recipe_id' and 'ingredient_ids'.
        df_ingr_map (pd.DataFrame): DataFrame mapping ingredient IDs ('id') to their names ('replaced').
        excluded_ingredients (set, optional): Ingredients to exclude. Defaults to common ingredients.
        top_n (int, optional): Number of top ingredients to return. Defaults to 10.

    Returns:
        pd.Series: Top `top_n` ingredients and their counts.
    """

    # Create a dictionary to map ingredient IDs to their simplified names
    ingr_map = df_ingr_map.set_index('id')['replaced'].to_dict()

    # Remove duplicate recipes
    unique_recipes = merged_df.drop_duplicates(subset='recipe_id')

    # Function to map ingredient IDs to simplified ingredient names
    def map_ingredient_ids(ids, ingr_map):
        if pd.isna(ids):
            return []
        try:
            return [ingr_map.get(int(ingr_id), 'Unknown') for ingr_id in ast.literal_eval(ids)]
        except (ValueError, SyntaxError):
            return []

    # Apply mapping to unique recipes
    unique_recipes['mapped_ingredients'] = unique_recipes['ingredient_ids'].apply(
        lambda x: map_ingredient_ids(x, ingr_map)
    )

    # Default list of ingredients to exclude
    if excluded_ingredients is None:
        excluded_ingredients = {'black pepper', 'vegetable oil', 'salt', 'pepper', 'olive oil', 'oil',
                                'butter', 'water', 'sugar', 'flour', 'brown sugar', 'salt and pepper',
                                'scallion', 'baking powder', 'garlic', 'flmy', 'garlic clove',
                                'all-purpose flmy', 'baking soda'}

    # Filter/count occurrences of ingredients
    filtered_ingredient_counts = (
        unique_recipes['mapped_ingredients']
        .explode()
        # Exclude common ingredients
        .loc[lambda x: ~x.isin(excluded_ingredients)]
        .value_counts()
        .head(top_n)
    )

    return filtered_ingredient_counts



def trendy_ingredients_by_seasons(df):
    dico_season_months = {'winter': ['01', '02', '03'], 'spring': [
        '04', '05', '06'], 'summer': ['07', '08', '09'], 'autumn': ['11', '12', '13']}

    dico_ingredients_seasons = {}
    for i in dico_season_months.keys():
        if i == 'winter':
            winter = main_values()


def add_season(df):
    """ Add a season column to the dataframe """
    def get_season(month):
        if month in ('12', '01', '02'):
            return 'winter'
        elif month in ('03', '04', '05'):
            return 'spring'
        elif month in ('06', '07', '08'):
            return 'summer'
        elif month in ('09', '10', '11'):
            return 'autumn'

    df['season'] = df['month_date'].map(get_season)
    return df


def count_recipes_season(df):
    """ Count recipes per season """
    if 'season' not in list(df.columns):
        df['season'] = add_season(df)

    # count recipes per season
    recipe_per_season = {'winter': len(df[df['season'] == 'winter']),
                         'spring': len(df[df['season'] == 'spring']),
                         'summer': len(df[df['season'] == 'summer']),
                         'autumn': len(df[df['season'] == 'autumn'])}

    return recipe_per_season

