import pandas as pd 

def add_columns(df_target, df_source, key_target, key_source, columns_to_add):
    """
    Ajoute des colonnes spécifiées d'un DataFrame source à un DataFrame cible en utilisant des clés spécifiées,
    sans inclure la colonne clé du DataFrame source dans le DataFrame final et en évitant les colonnes indésirables.

    Args:
        df_target (pd.DataFrame): DataFrame cible où les colonnes seront ajoutées.
        df_source (pd.DataFrame): DataFrame source contenant les colonnes à ajouter.
        key_target (str): Nom de la colonne clé dans le DataFrame cible.
        key_source (str): Nom de la colonne clé dans le DataFrame source.
        columns_to_add (list): Liste des colonnes à ajouter depuis le DataFrame source.

    Returns:
        pd.DataFrame: Le DataFrame cible avec les nouvelles colonnes ajoutées.
    """
    import pandas as pd

    # Vérification des colonnes clés
    if key_target not in df_target.columns:
        raise KeyError(f"La clé '{key_target}' n'est pas présente dans le DataFrame cible.")
    if key_source not in df_source.columns:
        raise KeyError(f"La clé '{key_source}' n'est pas présente dans le DataFrame source.")

    # Vérification des colonnes à ajouter
    missing_cols = [col for col in columns_to_add if col not in df_source.columns]
    if missing_cols:
        raise KeyError(f"Les colonnes suivantes sont manquantes dans le DataFrame source : {missing_cols}")

    # Sélectionner uniquement les colonnes nécessaires du DataFrame source
    df_source_reduced = df_source[[key_source] + columns_to_add].copy()

    # Supprimer la colonne 'id' du DataFrame cible si elle n'est pas la clé de jointure
    if key_source in df_target.columns and key_source != key_target:
        df_target = df_target.drop(columns=[key_source])

    # Effectuer la fusion sans créer de colonnes 'id_x' ou 'id_y'
    df_result = pd.merge(
        df_target,
        df_source_reduced,
        left_on=key_target,
        right_on=key_source,
        how='left'
    )

    # Supprimer la colonne clé du DataFrame source après la fusion uniquement si elle est différente de key_target
    if key_source != key_target:
        df_result = df_result.drop(columns=[key_source])

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
