import pandas as pd 

def add_columns(df_target, df_source, key_target, key_source, columns_to_add):
    """
    add columbs from a datafram source to a target dataframe with keys

    Args:
        df_target: Target DataFrame where columns will be add.
        df_source: Source DataFrame where containing the columns to add.
        key_target: Column name key in targeted Dataframe.
        key_source: Column name key in source Dataframe.
        columns_to_add: List of column to add from dataframe source.

    Raises:
        ValueError: if a datafram is not valid.
        KeyError: if the key or coulumn are not found.

    Returns:
        pd.DataFrame: Le DataFrame targeted with new columns.
    """
    # Vérifications de base
    if not isinstance(df_target, pd.DataFrame) or not isinstance(df_source, pd.DataFrame):
        raise ValueError("Les deux entrées doivent être des DataFrames pandas.")

    if key_target not in df_target.columns:
        raise KeyError(f"La clé '{key_target}' n'est pas présente dans le DataFrame cible.")

    if key_source not in df_source.columns:
        raise KeyError(f"La clé '{key_source}' n'est pas présente dans le DataFrame source.")

    if not all(col in df_source.columns for col in columns_to_add):
        raise KeyError(f"Les colonnes {columns_to_add} ne sont pas toutes présentes dans le DataFrame source.")

    # Fusion en ajoutant uniquement les colonnes spécifiées
    df_result = pd.merge(
        df_target,
        df_source[[key_source] + columns_to_add],
        left_on=key_target,
        right_on=key_source,
        how='left'
    )

    # Suppression de la clé du DataFrame source après fusion si elle est redondante
    if key_target != key_source:
        df_result.drop(columns=[key_source], inplace=True)

    return df_result

     
def drop_columns(df, columns_to_drop):
    """
    Function that drops columns

    Args:
        df : dataframe
        columns_to_drop (list, string): name of the column(s) to drop

    Returns:
        df: new dataframe without the columns that weren't needed 
    """
    # Vérifications de base
    if not isinstance(df, pd.DataFrame) :
        raise ValueError("Must be a dataframe")
    
    columns_to_drop= columns_to_drop if isinstance(columns_to_drop, list) else [columns_to_drop]

    for i in columns_to_drop:
        df=df.drop(i,axis=1)

    return df 

