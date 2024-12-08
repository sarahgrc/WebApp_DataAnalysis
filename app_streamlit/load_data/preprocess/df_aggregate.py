def df_aggregate(df):
    """
    Aggregates data to have one row per recipe_id, with the original columns (excluding 'user_id') plus:
    - num_users_commented: Number of unique users who commented on the recipe.
    - avg_reviews_per_user: Total number of reviews for the recipe.

    Args:
        df (pd.DataFrame): DataFrame containing recipe data, including 'recipe_id', 'user_id', and 'review'.

    Returns:
        pd.DataFrame: Aggregated DataFrame with one row per recipe_id, original columns (excluding 'user_id'),
                      and additional metrics.
    """

    aggregated_metrics = df.groupby('recipe_id').agg(
        num_comments=('user_id', 'nunique'),
        avg_ratings=('rating', 'mean')
    ).reset_index()

    
    unique_recipes = df.drop_duplicates(subset=['recipe_id']).reset_index(drop=True)

  
    unique_recipes = unique_recipes.drop(columns=['user_id','rating'])

 
    result = unique_recipes.merge(aggregated_metrics, on='recipe_id', how='left')

    return result