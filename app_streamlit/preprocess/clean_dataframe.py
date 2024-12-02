import pandas as pd

def prepare_final_dataframe(raw_interaction, raw_recipes, pp_recipes):
    """
    Prepare a new clean dataframe, that will be used for the analysis,
    by using other functions. 

    Args:
        raw_interaction (DataFrame): raw dataFrame of interactions from users 
        raw_recipes (DataFrame): raw dataFrame with recipes informations 
        pp_recipes (DataFrame): recipies dataFrame preprocessed

    Returns:
        df_merged (DataFrame): final dataFrame
    """

    # Step 1 : Merging raw_interaction and raw_recipes on "recipe_id" and "id" 
    # Rename 'id' to 'recipe_id' in raw_recipes 
    raw_recipes_renamed = raw_recipes.rename(columns={'id': 'recipe_id'})
    df_merged = pd.merge(raw_interaction, raw_recipes_renamed, on="recipe_id", how="left")

    # Step 2 : Add columns 'ingredient_ids', 'ingredient_tokens' from pp_recipes
    pp_recipes_renamed = pp_recipes.rename(columns={'id': 'recipe_id'})
    df_merged = pd.merge(
        df_merged,
        pp_recipes_renamed[['recipe_id', 'ingredient_ids', 'ingredient_tokens']],
        on="recipe_id",
        how="left"
    )

    # Step 3 : Separate columns "date" and "submitted" and remove useless columns
    if 'date' in df_merged.columns:
        df_merged[['year_date', 'month_date', 'day_date']] = df_merged['date'].str.split('-', expand=True)
        df_merged.drop(columns=['day_date', 'date'], inplace=True)  # Delete columns 'day_date' and 'date'

    if 'submitted' in df_merged.columns:
        df_merged[['year_submitted', 'month_submitted', 'day_submitted']] = df_merged['submitted'].str.split('-', expand=True)
        df_merged.drop(columns=['day_submitted', 'submitted'], inplace=True)  # Delete columns 'day_submitted' and 'submitted'

    # Step 4 : Cleaning data by removing outliers 
    if 'n_steps' in df_merged.columns:
        df_merged = df_merged[df_merged['n_steps'] <= 20]  # Keep values <= 20

    if 'minutes' in df_merged.columns:
        df_merged = df_merged[df_merged['minutes'] <= 240]  # Keep values <= 240

    # Step 5 : Remove columns "description" et "rating"
    columns_to_drop = ['description', 'rating']
    df_merged.drop(columns=[col for col in columns_to_drop if col in df_merged.columns], inplace=True)

    return df_merged

