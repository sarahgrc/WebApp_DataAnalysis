from code.preprocess.cleaning_data import *
from code.preprocess.merging import *
from tests.conftest import sample_raw_recipes
from code.preprocess.normalisation import *
from code.preprocess.add_column import *


def test_date_separated(sample_raw_recipes):
    """
    Teste la fonction `date_separated` sur un DataFrame d'échantillon.

    Vérifie que les colonnes spécifiques (`year`, `month`, `day`) sont 
    correctement ajoutées au DataFrame d'entrée, sans supprimer de colonnes 
    ou de lignes existantes.

    Args:
        sample_raw_recipes (pd.DataFrame): Un DataFrame contenant les données 
        brutes, y compris une colonne `submitted` qui sera séparée en 
        `year`, `month` et `day`.
    """
    assert len(sample_raw_recipes.columns) == 13  # Vérifie le nombre initial de colonnes
    d = date_separated('submitted', sample_raw_recipes)

    # Vérifie que les colonnes `year`, `month`, et `day` ont été ajoutées
    assert ('year' in d.columns)
    assert ('month' in d.columns)
    assert ('day' in d.columns)

    # Vérifie qu'aucune ligne n'a été supprimée
    assert len(d) == 200

    # Vérifie qu'aucune colonne n'a été supprimée et que 3 nouvelles colonnes ont été ajoutées
    assert len(d.columns) == len(sample_raw_recipes.columns) + 3


def test_outliers(outliers_sample):
    """
    Teste la fonction `outliers` pour détecter et extraire les valeurs aberrantes 
    dans un DataFrame d'échantillon.

    Vérifie le bon fonctionnement de la détection des valeurs aberrantes au-dessus 
    et en dessous des seuils donnés, ainsi que le retour des informations selon le 
    mode demandé.

    Args:
        outliers_sample (pd.DataFrame): Un DataFrame contenant des colonnes numériques 
        utilisées pour tester la détection des valeurs aberrantes.
    """
    # Teste les valeurs supérieures à un seuil donné
    outlier = outliers(outliers_sample, 'A', treshold_sup=30, treshold_inf=None, get_info=False)
    assert isinstance(outlier, list)  # Vérifie que le résultat est une liste
    assert len(outlier) == 6  # Vérifie le nombre de valeurs au-dessus du seuil

    # Teste les valeurs inférieures à un seuil donné
    outlier1 = outliers(outliers_sample, 'A', treshold_sup=None, treshold_inf=10, get_info=False)
    assert isinstance(outlier1, list)
    assert len(outlier1) == 4

    # Teste les valeurs dans une plage donnée avec retour des informations
    outlier2 = outliers(outliers_sample, 'A', treshold_sup=16, treshold_inf=37, get_info=True)
    assert isinstance(outlier2, pd.DataFrame)  # Vérifie que le résultat est un DataFrame
    assert len(outlier2) == 7  # Vérifie que les valeurs sont correctement filtrées


def test_df_merged(merged_sample):
    """
    Teste la fonction `dataframe_concat` pour la fusion de DataFrames.

    Vérifie que chaque type de jointure (`left`, `right`, `outer`, `inner`) 
    retourne un DataFrame avec la taille correcte.

    Args:
        merged_sample (tuple): Un tuple contenant deux DataFrames, partageant 
        une colonne commune `A` et des colonnes spécifiques (`B` ou `C`), 
        pour tester les différentes configurations de fusion.
    """
    df = [merged_sample[0], merged_sample[1]]

    # Vérifie que chaque type de jointure retourne le bon nombre de colonnes
    type_join = ["left", "right", "outer", "inner"]
    for i in type_join:
        merging = dataframe_concat(df, 'A', join=i)
        assert len(merging.columns) == 3

def test_normalisation(normalisation_data):
    """
    Tests the `normalisation` function to ensure it correctly normalizes 
    a numeric column in a DataFrame.

    The test checks that:
    - The normalized column is added to the DataFrame with the expected name.
    - The minimum value in the normalized column is 0.
    - The maximum value in the normalized column is 1.

    Args:
        normalisation_data (pd.DataFrame): A fixture providing a sample DataFrame 
                                           with a single numeric column.
    """
    result = normalisation(normalisation_data, 'value')
    assert 'value_normalisé' in result.columns
    assert result['value_normalisé'].iloc[0] == 0
    assert result['value_normalisé'].iloc[-1] == 1


def test_add_columns(column_merge_data):
    """
    Tests the `add_columns` function to ensure it correctly merges additional 
    columns from a source DataFrame into a target DataFrame based on a common key.

    The test verifies that:
    - The new column is successfully added to the target DataFrame.
    - Missing keys in the source DataFrame result in NaN values in the merged column.

    Args:
        column_merge_data (tuple): A fixture providing two DataFrames:
                                   - Target DataFrame with keys and values.
                                   - Source DataFrame with keys and additional columns to merge.
    """
    df_target, df_source = column_merge_data
    result = add_columns(df_target, df_source, 'key', 'key', ['extra'])
    assert 'extra' in result.columns
    assert result.loc[result['key'] == 3, 'extra'].isna().all()