import pandas as pd
from load_data.preprocess.df_aggregate import df_aggregate
from load_data.preprocess.merging import dataframe_concat
from load_data.preprocess.add_drop_column import add_columns
from load_data.preprocess.add_drop_column import drop_columns
from load_data.preprocess.cleaning_data import outliers_df
from load_data.preprocess.cleaning_data import date_separated
from load_data.preprocess.cleaning_data import add_season
from analyse.utils import nutri_score

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

    missing_recipes = raw_recipes[raw_recipes['name'].isna()]
    print(missing_recipes)
    print(missing_recipes.shape)
    print(raw_recipes.columns)

    # In order to avoid memory error on streamlit
    batch_size = 50000  # Nombre de lignes à traiter à la fois
    chunks = []
    for i in range(0, len(raw_recipes), batch_size):
        chunk = raw_recipes.iloc[i:i + batch_size].copy()
    
        # Extraction des colonnes de nutrition
        chunk[['Calories', 'Total Fat', 'Sugar', 'Sodium', 'Protein', 'Saturated Fat', 'Carbohydrates']] = \
            chunk['nutrition'].str.strip('[]').str.split(',', expand=True)
        
        # Conversion des colonnes nutritionnelles en float
        nutrition_cols = ['Calories', 'Total Fat', 'Sugar', 'Sodium', 'Protein', 'Saturated Fat', 'Carbohydrates']
        chunk[nutrition_cols] = chunk[nutrition_cols].apply(pd.to_numeric, errors='coerce')
        
        # Calcul du Nutri-Score pour chaque chunk
        chunk['nutri_score'] = chunk.apply(nutri_score, axis=1)
        
    # Ajouter le chunk traité à la liste
    chunks.append(chunk)

    # Recombine the chunks after treatment
    raw_recipes = pd.concat(chunks, ignore_index=True)
    nutrition_cols = ['Calories', 'Total Fat', 'Sugar', 'Sodium', 'Protein', 'Saturated Fat', 'Carbohydrates']
    raw_recipes[nutrition_cols] = raw_recipes['nutrition'].str.strip('[]').str.split(',', expand=True)
    # Convert col in type float 
    raw_recipes[nutrition_cols] = raw_recipes[nutrition_cols].apply(pd.to_numeric, errors='coerce')

  



    # Colomns to filter
    columns_to_filter = ["Calories", "Total Fat", "Sugar", "Sodium", "Protein", "Saturated Fat", "Carbohydrates"]

    # Apply thresholds of 95%
    for col in columns_to_filter:
        lower_bound = raw_recipes[col].quantile(0.025)  # 2.5% percentile
        upper_bound = raw_recipes[col].quantile(0.975)  # 97.5% percentile

        # Filter values outside of the bounds
        raw_recipes = raw_recipes[(raw_recipes[col] >= lower_bound) & (raw_recipes[col] <= upper_bound)]


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
        df_merged = df_merged[~df_merged['minutes'].isin(outliers_minutes)]
        df_merged.reset_index(drop=True, inplace=True)

    # step 5 : delate unusfull columns
    columns_to_drop = ['description']
    df_merged = drop_columns(df_merged, columns_to_drop)
    df_merged = df_aggregate(df_merged)

    # step 6 : add a column for seasons 
    df_merged=add_season(df_merged)     



    return df_merged
