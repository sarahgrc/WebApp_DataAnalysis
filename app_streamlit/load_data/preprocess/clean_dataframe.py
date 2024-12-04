import pandas as pd
from load_data.preprocess.df_aggregate import df_aggregate
from load_data.preprocess.merging import dataframe_concat
from load_data.preprocess.add_drop_column import add_columns
from load_data.preprocess.add_drop_column import drop_columns
from load_data.preprocess.cleaning_data import outliers_df
from load_data.preprocess.cleaning_data import date_separated



def prepare_final_dataframe(raw_interaction, raw_recipes, pp_recipes):
    """
    Prépare un nouveau DataFrame propre qui sera utilisé pour l'analyse,
    en utilisant d'autres fonctions.

    Args:
        raw_interaction (DataFrame): DataFrame brute des interactions des utilisateurs.
        raw_recipes (DataFrame): DataFrame brute avec les informations des recettes.
        pp_recipes (DataFrame): DataFrame pré-traitée des recettes.

    Returns:
        df_merged (DataFrame): DataFrame finale prête pour l'analyse.
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

    # Step 4 : clean dataframe
    if 'n_steps' in df_merged.columns:
        df_merged.reset_index(drop=True, inplace=True)
        outliers_n_steps = outliers_df(df_merged, 'n_steps', treshold_sup=20)
        df_merged = df_merged[~df_merged['n_steps'].isin(outliers_n_steps)]
        df_merged.reset_index(drop=True, inplace=True)

    if 'minutes' in df_merged.columns:
        df_merged.reset_index(drop=True, inplace=True)
        outliers_minutes = outliers_df(df_merged, 'minutes', treshold_sup=240)
        df_merged = df_merged[~df_merged['minutes'].isin(outliers_minutes)]s
        df_merged.reset_index(drop=True, inplace=True)

    # step 5 : delate unusfull columns
    columns_to_drop = ['description']
    df_merged = drop_columns(df_merged, columns_to_drop)
    df_merged = df_aggregate(df_merged)

    return df_merged
