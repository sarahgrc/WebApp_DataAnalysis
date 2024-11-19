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

    recipe_counts = df.groupby('contributor_id')['recipe_id'].nunique()
    bins = [0, 1, 5, 8, float('inf')]
    labels = ['1 recette', '2 à 5 recettes', '6 à 8 recettes', 'Plus de 10 recettes']

    binned_counts = pd.cut(recipe_counts, bins=bins, labels=labels, right=True)

    contributor_counts_by_bin = binned_counts.value_counts().sort_index()

    return contributor_counts_by_bin

def top_contributors_by_recipes(df, top_n=10):
    """
    Returns the top X contributors who have published the most unique recipes.

    Parameters:
    - df (pd.DataFrame): A DataFrame containing recipe data.
    - top_n (int): Number of top contributors to return.

    Returns:
    - pd.Series: The `top_n` contributors with the count of unique recipes they have published.
    """
    # Remove duplicate
    unique_recipes_df = df.drop_duplicates(subset='recipe_id')
    
    top_contributors = unique_recipes_df['contributor_id'].value_counts().head(top_n)
    return top_contributors

def top_contributors_by_commented_recipes(df, top_n=10):
    """
    Returns the top X contributors whose recipes received the most comments.

    Parameters:
    - df (pd.DataFrame): A DataFrame containing recipe data.
    - top_n (int): Number of top contributors to return.

    Returns:
    - pd.Series: The `top_n` contributors with the total number of comments on their recipes.
    """
    commented_recipes = df.dropna(subset=['review'])
    comments_per_contributor = commented_recipes.groupby('contributor_id')['recipe_id'].count().sort_values(ascending=False).head(top_n)
    
    return comments_per_contributor

def top_tags_recipes(df, top_n=20):
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
    tags_series = df['tags'].apply(eval).explode()
    
    # Count the most frequent tags
    top_tags_recipes = tags_series.value_counts().head(top_n)
    return top_tags_recipes

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
    commented_recipes = df.dropna(subset=['review'])

    most_commented = commented_recipes['recipe_id'].value_counts().head(top_recipes).index

    # Filter for these recipes
    filtered_df = df[df['recipe_id'].isin(most_commented)]
    

    tags_series = filtered_df['tags'].apply(eval).explode()
    top_tags = tags_series.value_counts().head(top_n)
    return top_tags

import pandas as pd

def get_top_ingredients(final_df, ingr_map_path, excluded_ingredients=None, top_n=10):
    """
    Identifies the most frequently used ingredients after excluding common ingredients.

    Parameters:
    - final_df (pd.DataFrame): Preloaded DataFrame containing recipe data.
    - ingr_map_path (str): Path to the ingr_map.pkl file.
    - excluded_ingredients (set): Set of ingredients to exclude. Default is a set of common ingredients.
    - top_n (int): Number of top ingredients to display.

    Returns:
    - pd.Series: The `top_n` most frequently used ingredients.
    """
    # Load ingr_map.pkl
    df_ingr_map = pd.read_pickle(ingr_map_path)

    # Create a dictionary to map ingredient IDs to their simplified names
    ingr_map = df_ingr_map.set_index('id')['replaced'].to_dict()  # Replace 'replaced' with 'processed' if necessary

    # Remove duplicate recipes
    unique_recipes = final_df.drop_duplicates(subset='recipe_id')

    # Function to map ingredient IDs to simplified ingredient names
    def map_ingredient_ids(ids, ingr_map):
        if pd.isna(ids):
            return []
        try:
            return [ingr_map.get(int(ingr_id), 'Unknown') for ingr_id in eval(ids)]
        except (ValueError, SyntaxError):
            return []

    # Apply mapping to unique recipes
    unique_recipes['mapped_ingredients'] = unique_recipes['ingredient_ids'].apply(lambda x: map_ingredient_ids(x, ingr_map))

    # Default list of ingredients to exclude
    if excluded_ingredients is None:
        excluded_ingredients = {'black pepper', 'vegetable oil', 'salt', 'pepper', 'olive oil', 'oil', 
                                'butter', 'water', 'sugar', 'flour', 'brown sugar', 'salt and pepper', 
                                'scallion', 'baking powder', 'garlic', 'flmy', 'garlic clove', 
                                'all-purpose flmy', 'baking soda'}

    # Filter and count occurrences of ingredients
    filtered_ingredient_counts = (
        unique_recipes['mapped_ingredients']
        .explode()
        .loc[lambda x: ~x.isin(excluded_ingredients)]  # Exclude common ingredients
        .value_counts()
        .head(top_n)
    )

    return filtered_ingredient_counts