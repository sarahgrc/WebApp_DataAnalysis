import pandas as pd
from ..preprocess.df_aggregate import df_aggregate
from ..preprocess.merging import dataframe_concat
from ..preprocess.add_drop_column import add_columns
from ..preprocess.add_drop_column import drop_columns
from ..preprocess.cleaning_data import outliers_df
from ..preprocess.cleaning_data import remove_outliers_iqr
from ..preprocess.cleaning_data import date_separated
from ..preprocess.cleaning_data import add_season
from ...analyse.utils import nutri_score
import logging 

logging.basicConfig(
    filename='logging/debug.log',
    level=logging.DEBUG,
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

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

    logging.info("Starting to prepare the final dataframe.")

    # step 1 : merge raw_interaction et raw_recipes on "recipe_id" et "id"

    raw_recipes_renamed = raw_recipes.rename(columns={'id': 'recipe_id'})

    df_merged = dataframe_concat([raw_interaction, raw_recipes_renamed], key='recipe_id', join="left")
    df_merged.reset_index(drop=True, inplace=True)
    logging.info("Merged raw_interaction with raw_recipes on 'recipe_id'.")


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
    df_merged=df_merged.head(50000) #not enough ram for less 
    logging.info("Added 'ingredient_ids' and 'ingredient_tokens' columns from pp_recipes.")

    # step 3 : seperate date and submitted and delete column
    if 'date' in df_merged.columns:
        df_merged = date_separated('date', df_merged)
        df_merged = drop_columns(df_merged, ['day', 'date'])
        logging.info("Separated 'date' column and dropped 'day' and 'date'.")

    if 'submitted' in df_merged.columns:
        df_merged = date_separated('submitted', df_merged)
        df_merged = drop_columns(df_merged, ['day', 'submitted'])
        logging.info("Removed outliers from 'n_steps' column.")
    df_merged.reset_index(drop=True, inplace=True)

    # cleaning intermediate
    if 'n_steps' in df_merged.columns:
        df_merged.reset_index(drop=True, inplace=True)
        outliers_n_steps = outliers_df(df_merged, 'n_steps', treshold_sup=20)
        df_merged = df_merged[~df_merged['n_steps'].isin(outliers_n_steps)]
        df_merged.reset_index(drop=True, inplace=True)

    if 'minutes' in df_merged.columns:
        df_merged.reset_index(drop=True, inplace=True)
        outliers_minutes = outliers_df(df_merged, 'minutes', treshold_sup=240)
        df_merged = df_merged[~df_merged['minutes'].isin(outliers_minutes)]
        df_merged.reset_index(drop=True, inplace=True)

    # step 5 : delate unusfull columns
    columns_to_drop = ['description']
    df_merged = drop_columns(df_merged, columns_to_drop)
    df_merged = df_aggregate(df_merged)
    logging.info("Dropped 'description' column and applied aggregation.")

    # step 6 : add a column for seasons
    df_merged=add_season(df_merged)
    logging.info("Added 'season' column.")


    # step 7: Nutrients data treatment
    nutrition_cols = ['Calories', 'Total Fat', 'Sugar', 'Sodium', 'Protein', 'Saturated Fat', 'Carbohydrates']
    df_merged[nutrition_cols] = df_merged['nutrition'].str.strip('[]').str.split(',', expand=True)
    # Conversion in float
    df_merged[nutrition_cols] = df_merged[nutrition_cols].apply(pd.to_numeric, errors='coerce')
    # Calcul the nutrii-score
    df_merged['nutri_score'] = df_merged.apply(nutri_score, axis=1)
    logging.info("Added 'season' column.")


    # Step 8 : clean dataframe (supprimer les outliers après traitement de 'nutrition')
    columns_to_check_outliers = [
        'recipe_id', 'minutes', 'contributor_id', 'n_steps', 'n_ingredients',
        'Calories', 'Total Fat', 'Sugar', 'Sodium', 'Protein', 'Saturated Fat', 'Carbohydrates'
    ]

    for col in columns_to_check_outliers:
        if col in df_merged.columns:
            df_merged = remove_outliers_inter(df_merged, col)
    logging.info("Removed outliers from 'nutrition' columns.")


    logging.info("Final dataframe prepared successfully.")
    

    return df_merged

