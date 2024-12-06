import pandas as pd
from analyse.utils import calculate_negative_points_nutri_score, calculate_positive_points_nutri_score, nutri_score

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

    batch_size = 50000  # Nombre de lignes à traiter à la fois
    chunks = []

    for i in range(0, len(raw_recipes), batch_size):
        chunk = raw_recipes.iloc[i:i+batch_size].copy()
        chunk[['Calories', 'Total Fat', 'Sugar', 'Sodium', 'Protein', 'Saturated Fat', 'Carbohydrates']] = \
            chunk['nutrition'].str.strip('[]').str.split(',', expand=True)
        chunks.append(chunk)

    # Recombinez les morceaux après traitement
    raw_recipes = pd.concat(chunks, ignore_index=True)


    nutrition_cols = ['Calories', 'Total Fat', 'Sugar', 'Sodium', 'Protein', 'Saturated Fat', 'Carbohydrates']

    raw_recipes[nutrition_cols] = raw_recipes['nutrition'].str.strip('[]').str.split(',', expand=True)

    # Convertir les colonnes en type float (plus efficace que object)
    raw_recipes[nutrition_cols] = raw_recipes[nutrition_cols].apply(pd.to_numeric, errors='coerce')


    # Colomns to filter
    columns_to_filter = ["Calories", "Total Fat", "Sugar", "Sodium", "Protein", "Saturated Fat", "Carbohydrates"]

    # Apply thresholds of 95%
    for col in columns_to_filter:
        lower_bound = raw_recipes[col].quantile(0.025)  # 2.5% percentile
        upper_bound = raw_recipes[col].quantile(0.975)  # 97.5% percentile

        # Filter values outside of the bounds
        raw_recipes = raw_recipes[(raw_recipes[col] >= lower_bound) & (raw_recipes[col] <= upper_bound)]

    print("Nutrition treatment done!!!")

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

    # Step 5 : Remove columns "description" 
    columns_to_drop = ['description']
    df_merged.drop(columns=[col for col in columns_to_drop if col in df_merged.columns], inplace=True)





    print("Merged df head : ")
    print(df_merged.head())
    


    return df_merged

