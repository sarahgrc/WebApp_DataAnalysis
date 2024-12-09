import logging 

logging.basicConfig(
    filename='logging/debug.log',
    level=logging.DEBUG,
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def df_aggregate(df):
    """
    Aggregates data to have one row per recipe_id, with the original columns (excluding 'user_id') plus:
    - num_comments: Number of unique users who commented on the recipe.
    - avg_reviews_per_user: Total number of reviews for the recipe.

    Args:
        df (pd.DataFrame): DataFrame containing recipe data, including 'recipe_id', 'user_id', and 'review'.

    Returns:
        pd.DataFrame: Aggregated DataFrame with one row per recipe_id, original columns (excluding 'user_id'),
                      and additional metrics.
    """

    logging.info("Running df_aggregate function")

    try:
        # Aggregate metrics
        logging.info("Aggregating metrics for each recipe_id")
        aggregated_metrics = df.groupby('recipe_id').agg(
            num_comments=('user_id', 'nunique'),
            avg_ratings=('rating', 'mean')
        ).reset_index()

        # Drop duplicate recipes
        logging.info("Dropping duplicate rows based on recipe_id")
        unique_recipes = df.drop_duplicates(subset=['recipe_id']).reset_index(drop=True)

        # Drop 'user_id' and 'rating' columns
        logging.info("Removing unnecessary columns: 'user_id' and 'rating'")
        unique_recipes = unique_recipes.drop(columns=['user_id', 'rating'])

        # Merge the metrics with unique recipes
        logging.info("Merging aggregated metrics with the unique recipes dataframe")
        result = unique_recipes.merge(aggregated_metrics, on='recipe_id', how='left')

        logging.info(f"Successfully aggregated dataframe. Resulting shape: {result.shape}")
        return result

    except Exception as e:
        logging.error(f"Error in df_aggregate: {e}")
        raise
