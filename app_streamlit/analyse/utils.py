    """functions used for statistics
    """
import ast
import pandas as pd

def metrics_main_contributor(df):
    """
    Calculate the total number of unique contributors and recipes in the dataset.

    Args:
        df (pd.DataFrame): DataFrame containing recipe data.

    Returns:
        tuple: Number of unique contributors and recipes.
    """
    num_contributors = df['contributor_id'].nunique()
    num_recipes = df['recipe_id'].nunique()
    return num_contributors, num_recipes

def average_and_total_comments_per_contributor(df):
    """
    Calculate the average and total number of comments per contributor.

    Args:
        df (pd.DataFrame): DataFrame containing 'contributor_id' and 'num_comments'.

    Returns:
        pd.DataFrame: DataFrame with 'contributor_id', 'avg_comments_per_recipe', and 'total_comments'.
    """
    if 'contributor_id' not in df.columns or 'num_comments' not in df.columns:
        raise ValueError("The DataFrame must contain 'contributor_id' and 'num_comments'.")

    df['contributor_id'] = df['contributor_id'].astype(str)

    stats = df.groupby('contributor_id')['num_comments'].agg(
        avg_comments_per_recipe='mean',
        total_comments='sum'
    ).reset_index()

    stats = stats.sort_values(by='avg_comments_per_recipe', ascending=False)
    return stats

def top_commented_recipes_by_contributors(df, top_contributors, max_recipes_per_contributor=5):
    """
    Extract top commented recipes for each contributor in the top contributors list.

    Args:
        df (pd.DataFrame): DataFrame containing recipe data.
        top_contributors (pd.DataFrame): DataFrame of top contributors.
        max_recipes_per_contributor (int): Maximum number of recipes per contributor.

    Returns:
        pd.DataFrame: DataFrame containing contributor IDs, recipe IDs, names, and number of comments.
    """
    required_columns = {'contributor_id', 'recipe_id', 'name', 'num_comments'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"The DataFrame must contain columns: {required_columns}.")

    df['contributor_id'] = df['contributor_id'].astype(str)
    top_contributors['contributor_id'] = top_contributors['contributor_id'].astype(str)

    filtered_df = df[df['contributor_id'].isin(top_contributors['contributor_id'])]
    filtered_df = filtered_df.sort_values(by='num_comments', ascending=False)

    top_recipes = (
        filtered_df.groupby('contributor_id')
        .head(max_recipes_per_contributor)
        .reset_index(drop=True)
    )

    return top_recipes[['contributor_id', 'recipe_id', 'name', 'num_comments']]

def count_contributors_by_recipe_range_with_bins(df):
    """
    Categorize contributors based on the number of unique recipes they contributed.

    Args:
        df (pd.DataFrame): DataFrame containing 'recipe_id' and 'contributor_id'.

    Returns:
        pd.Series: Series with recipe range categories as index and contributor counts as values.
    """
    recipe_counts = df.groupby('contributor_id')['recipe_id'].nunique()
    bins = [0, 1, 5, 8, float('inf')]
    labels = ['1 recipe', '2-5 recipes', '6-8 recipes', '> 8 recipes']

    binned_counts = pd.cut(recipe_counts, bins=bins, labels=labels, right=True)
    return binned_counts.value_counts().sort_index()

def top_commented_recipes(df, top_n=10):
    """
    Extract the top N recipes with the highest number of comments.

    Args:
        df (pd.DataFrame): DataFrame containing recipe data.
        top_n (int): Number of top recipes to return.

    Returns:
        pd.DataFrame: DataFrame containing top N recipes.
    """
    return df.sort_values(by='num_comments', ascending=False).head(top_n)[
        ['contributor_id', 'recipe_id', 'num_comments', 'name']
    ]

def get_top_tags(df, most_commented=False, top_recipes=20, top_n=10):
    """
    Retrieve the most frequently used tags.

    Args:
        df (pd.DataFrame): DataFrame containing recipe data.
        most_commented (bool): Whether to filter by the most commented recipes.
        top_recipes (int): Number of top recipes to consider if most_commented is True.
        top_n (int): Number of tags to return.

    Returns:
        pd.Series: Top N most frequently used tags.
    """
    if most_commented:
        most_commented_df = df.sort_values(by='num_comments', ascending=False).head(top_recipes)
        filtered_df = df[df['recipe_id'].isin(most_commented_df['recipe_id'])]
    else:
        filtered_df = df

    tags_series = filtered_df['tags'].apply(eval).explode()
    return tags_series.value_counts().head(top_n)

def get_top_ingredients2(df, df_ingr_map, excluded_ingredients=None, top_n=10):
    """
    Find the most frequently used ingredients, excluding common ones.

    Args:
        df (pd.DataFrame): DataFrame with recipe data.
        df_ingr_map (pd.DataFrame): DataFrame mapping ingredient IDs to their names.
        excluded_ingredients (set, optional): Ingredients to exclude.
        top_n (int): Number of top ingredients to return.

    Returns:
        pd.Series: Top N ingredients and their counts.
    """
    ingr_map = df_ingr_map.set_index('id')['replaced'].to_dict()

    def map_ingredient_ids(ids):
        if pd.isna(ids):
            return []
        try:
            return [ingr_map.get(int(ingr_id), 'Unknown') for ingr_id in ast.literal_eval(ids)]
        except (ValueError, SyntaxError):
            return []

    df['mapped_ingredients'] = df['ingredient_ids'].apply(map_ingredient_ids)

    if excluded_ingredients is None:
        excluded_ingredients = {
            'black pepper', 'vegetable oil', 'salt', 'pepper', 'olive oil',
            'butter', 'water', 'sugar', 'flour', 'brown sugar',
        }

    filtered_ingredients = (
        df['mapped_ingredients']
        .explode()
        .loc[lambda x: ~x.isin(excluded_ingredients)]
        .value_counts()
        .head(top_n)
    )

    return filtered_ingredients

def count_recipes_season(df):
    """
    Count recipes per season.

    Args:
        df (pd.DataFrame): DataFrame with recipe data and a 'season' column.

    Returns:
        dict: Recipe counts per season.
    """
    return {
        'winter': len(df[df['season'] == 'winter']),
        'spring': len(df[df['season'] == 'spring']),
        'summer': len(df[df['season'] == 'summer']),
        'autumn': len(df[df['season'] == 'autumn']),
    }

def count_recipes_per_user(df):
    """
    Count the number of unique recipes per user.

    Args:
        df (pd.DataFrame): DataFrame containing 'recipe_id' and 'contributor_id'.

    Returns:
        pd.Series: Series with contributor IDs as index and recipe counts as values.
    """
    return df.groupby('contributor_id')['recipe_id'].nunique()
