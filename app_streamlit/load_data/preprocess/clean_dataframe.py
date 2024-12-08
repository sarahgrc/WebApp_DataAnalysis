import pandas as pd
from load_data.preprocess.df_aggregate import df_aggregate
from load_data.preprocess.merging import dataframe_concat
from load_data.preprocess.add_drop_column import add_columns
from load_data.preprocess.add_drop_column import drop_columns
from load_data.preprocess.cleaning_data import outliers_df
from load_data.preprocess.cleaning_data import date_separated
from load_data.preprocess.cleaning_data import add_season
from analyse.utils import nutri_score
from load_data.preprocess.cleaning_data import remove_outliers_iqr

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

    # step 1 : merge raw_interaction et raw_recipes on "recipe_id" et "id"
    raw_recipes_renamed = raw_recipes.rename(columns={'id': 'recipe_id'})
    
    df_merged = dataframe_concat([raw_interaction, raw_recipes_renamed], key='recipe_id', join="left")
    df_merged.reset_index(drop=True, inplace=True)
    

    # step 2 : add columns 'ingredient_ids', 'ingredient_tokens' on pp_recipes
    pp_recipes_renamed = pp_recipes.rename(columns={'id': 'recipe_id'})
    df_merged = add_columns(
        df_merged,
        pp_recipes_renamed,
        key_target='recipe_id',
        key_source='recipe_id',
        columns_to_add=['ingredient_ids', 'ingredient_tokens']
    )

    df_merged.reset_index(drop=True, inplace=True)

    # step 3 : seperate date and submitted and delete column
    if 'date' in df_merged.columns:
        df_merged = date_separated('date', df_merged)
        df_merged = drop_columns(df_merged, ['day', 'date'])

    if 'submitted' in df_merged.columns:
        df_merged = date_separated('submitted', df_merged)
        df_merged = drop_columns(df_merged, ['day', 'submitted'])

    
    df_merged.reset_index(drop=True, inplace=True)

    #first cleaning
    if 'minutes' in df_merged.columns:
        df_merged.reset_index(drop=True, inplace=True)
        outliers_minutes = outliers_df(df_merged, 'minutes', treshold_sup=240)
        df_merged = df_merged[~df_merged['minutes'].isin(outliers_minutes)]
        df_merged.reset_index(drop=True, inplace=True)

    # step 5 : delate unusfull columns
    columns_to_drop = ['description']
    df_merged = drop_columns(df_merged, columns_to_drop)
    df_merged = df_aggregate(df_merged)

    # step 6 : add a column for seasons
    df_merged=add_season(df_merged)  


    # step 7: Nutrients data treatment
    nutrition_cols = ['Calories', 'Total Fat', 'Sugar', 'Sodium', 'Protein', 'Saturated Fat', 'Carbohydrates']
    df_merged[nutrition_cols] = df_merged['nutrition'].str.strip('[]').str.split(',', expand=True)
    # Conversion in float
    df_merged[nutrition_cols] = df_merged[nutrition_cols].apply(pd.to_numeric, errors='coerce')
    # Calcul the nutrii-score
    df_merged['nutri_score'] = df_merged.apply(nutri_score, axis=1)


    # Step 8 : clean dataframe (supprimer les outliers après traitement de 'nutrition')
    columns_to_check_outliers = [
        'recipe_id', 'minutes', 'contributor_id', 'n_steps', 'n_ingredients',
        'Calories', 'Total Fat', 'Sugar', 'Sodium', 'Protein', 'Saturated Fat', 'Carbohydrates'
    ]

    def remove_outliers_inter(df, column):
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        inter = q3 - q1
        lower_bound = q1 - 1.5 * inter
        upper_bound = q3 + 1.5 * inter
        return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

    for col in columns_to_check_outliers:
        if col in df_merged.columns:
            df_merged = remove_outliers_inter(df_merged, col)


    return df_merged
