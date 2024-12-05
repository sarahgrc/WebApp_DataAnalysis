"""Function used for statistics. 
"""
import ast
import pandas as pd
from .classification_values import main_values


def metrics_main_contributor(df):
    num_contributors = df['contributor_id'].nunique()
    num_recipes = df['recipe_id'].nunique()
    return num_contributors, num_recipes

def average_and_total_comments_per_contributor(df):
    """
    Calculates the average number of comments per recipe and the total number of comments for each contributor.

    Parameters:
    - df (pd.DataFrame): A DataFrame containing recipe data, including 'contributor_id' and 'num_comments'.

    Returns:
    - pd.DataFrame: A DataFrame with 'contributor_id', 'avg_comments_per_recipe', and 'total_comments',
      where contributor_id is treated as a category.
    """
    # Vérifier que les colonnes nécessaires existent
    if 'contributor_id' not in df.columns or 'num_comments' not in df.columns:
        raise ValueError("Le DataFrame doit contenir les colonnes 'contributor_id' et 'num_comments'.")

    # Convertir contributor_id en chaîne
    df['contributor_id'] = df['contributor_id'].astype(str)

    # Calculer la moyenne des commentaires et le total des commentaires par contributeur
    stats = df.groupby('contributor_id')['num_comments'].agg(
        avg_comments_per_recipe='mean',  # Moyenne des commentaires
        total_comments='sum'            # Total des commentaires
    ).reset_index()

    # Renommer les colonnes pour plus de clarté
    stats.columns = ['contributor_id', 'avg_comments_per_recipe', 'total_comments']

    # Trier par moyenne décroissante
    stats = stats.sort_values(by='avg_comments_per_recipe', ascending=False)

    return stats


def top_commented_recipes_by_contributors(df, top_contributors, max_recipes_per_contributor=5):
    """
    Extracts the top commented recipes for each contributor in the top contributors list.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing recipe data.
    - top_contributors (pd.DataFrame): A DataFrame containing the IDs of the top contributors.
    - max_recipes_per_contributor (int): Maximum number of recipes to return per contributor.

    Returns:
    - pd.DataFrame: A DataFrame containing contributor IDs, recipe IDs, names, and number of comments.
    """
    # Vérifier les colonnes nécessaires
    if not {'contributor_id', 'recipe_id', 'name', 'num_comments'}.issubset(df.columns):
        raise ValueError("Le DataFrame doit contenir les colonnes 'contributor_id', 'recipe_id', 'name', et 'num_comments'.")

    # Convertir contributor_id en chaîne dans les deux DataFrames
    df['contributor_id'] = df['contributor_id'].astype(str)
    top_contributors['contributor_id'] = top_contributors['contributor_id'].astype(str)

    # Filtrer les recettes appartenant aux top contributeurs
    filtered_df = df[df['contributor_id'].isin(top_contributors['contributor_id'])]
    
    # Trier les recettes par nombre de commentaires
    filtered_df = filtered_df.sort_values(by='num_comments', ascending=False)
    
    # Limiter le nombre de recettes par contributeur
    top_recipes = (
        filtered_df.groupby('contributor_id')
        .head(max_recipes_per_contributor)
        .reset_index(drop=True)
    )
    
    # Sélectionner les colonnes pertinentes
    return top_recipes[['contributor_id', 'recipe_id', 'name', 'num_comments']]


def count_contributors_by_recipe_range_with_bins(df):
    """
    Categorizes contributors based on the number of unique recipes they have contributed 
    and counts how many contributors fall into each category.

    Parameters:
    - df (pd.DataFrame): A DataFrame containing recipe data, including 'recipe_id' and 'contributor_id'.

    Returns:
    - pd.Series: A series where the index represents the recipe range categories 
      and the values are the counts of contributors in each category.

    The recipe ranges (bins) and their corresponding labels:
    - '1 recipe': Contributors with exactly 1 unique recipe.
    - '2 to 5 recipes': Contributors with 2 to 5 unique recipes.
    - '6 to 8 recipes': Contributors with 6 to 8 unique recipes.
    - 'More than 8 recipes': Contributors with more than 8 unique recipes.
    """

    # Compter le nombre de recettes uniques par contributeur
    recipe_counts = df.groupby('contributor_id')['recipe_id'].nunique()

    # Définir les plages de recettes (bins)
    bins = [0, 1, 5, 8, float('inf')]
    labels = ['1 recipe', '2-5 recipes', '6-8 recipes', '> 8 recipes']

    # Découper en catégories
    binned_counts = pd.cut(recipe_counts, bins=bins, labels=labels, right=True)

    # Compter le nombre de contributeurs dans chaque bin
    contributor_counts_by_bin = binned_counts.value_counts().sort_index()

    return contributor_counts_by_bin


def top_commented_recipes(df, top_n=10):
    """
    Extracts the top N recipes with the highest number of comments, including the contributor and recipe details.

    Parameters:
    - df (pd.DataFrame): A DataFrame containing recipe data, including 'recipe_id', 'contributor_id', and 'num_comments'.
    - top_n (int): The number of top recipes to return.

    Returns:
    - pd.DataFrame: A DataFrame containing 'contributor_id', 'recipe_id', and 'num_comments' for the top N recipes.
    """
    # Appeler la fonction d'agrégation pour obtenir un DataFrame unique par recette


    # Trier par 'num_comments' en ordre décroissant et sélectionner les top N
    top_recipes = df.sort_values(by='num_comments', ascending=False).head(top_n)

    # Garder uniquement les colonnes 'contributor_id', 'recipe_id' et 'num_comments'
    result = top_recipes[['contributor_id', 'recipe_id', 'num_comments','name']]

    return result

def top_commented_recipes_by_contributors(df, top_contributors, max_recipes_per_contributor=5):
    """
    Extracts the top commented recipes for each contributor in the top contributors list.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing recipe data.
    - top_contributors (pd.DataFrame): A DataFrame containing the IDs of the top contributors.
    - max_recipes_per_contributor (int): Maximum number of recipes to return per contributor.

    Returns:
    - pd.DataFrame: A DataFrame containing contributor IDs, recipe IDs, names, and number of comments.
    """
    # Vérifier les colonnes nécessaires
    if not {'contributor_id', 'recipe_id', 'name', 'num_comments'}.issubset(df.columns):
        raise ValueError("Le DataFrame doit contenir les colonnes 'contributor_id', 'recipe_id', 'name', et 'num_comments'.")
    
    # Filtrer les recettes appartenant aux top contributeurs
    filtered_df = df[df['contributor_id'].isin(top_contributors['contributor_id'])]
    
    # Trier les recettes par nombre de commentaires
    filtered_df = filtered_df.sort_values(by='num_comments', ascending=False)
    
    # Limiter le nombre de recettes par contributeur
    top_recipes = (
        filtered_df.groupby('contributor_id')
        .head(max_recipes_per_contributor)
        .reset_index(drop=True)
    )
    
    # Sélectionner les colonnes pertinentes
    return top_recipes[['contributor_id', 'recipe_id', 'name', 'num_comments']]



def get_top_tags(df, most_commented=False, top_recipes=20, top_n=10):
    """
    Returns the most frequently used tags either for all recipes or for the top most commented recipes.

    Parameters:
    - df (pd.DataFrame): A DataFrame containing recipe data.
    - most_commented (bool): If True, only consider the most commented recipes.
    - top_recipes (int): Number of most commented recipes to consider (used only if most_commented=True).
    - top_n (int): Number of most frequent tags to return.

    Returns:
    - pd.Series: The `top_n` most frequently used tags.
    """

    if most_commented:
        # Identifier les recettes les plus commentées
        most_commented = df.sort_values(by='num_comments', ascending=False).head(top_recipes)
        filtered_df = df[df['recipe_id'].isin(most_commented['recipe_id'])]
    else:
        # Utiliser toutes les recettes
        filtered_df = df

    # Exploser les tags et compter
    tags_series = filtered_df['tags'].apply(eval).explode()
    top_tags = tags_series.value_counts().head(top_n)

    return top_tags


def top_contributors_by_recipes(df, top_n=10):
    """
    Finds the top contributors with the highest number of recipes in the dataset.

    Parameters:
    - df (pd.DataFrame): A DataFrame containing recipe data, including 'contributor_id'.
    - top_n (int): Number of top contributors to return.

    Returns:
    - pd.DataFrame: A DataFrame containing the top contributors and their total number of recipes.
    """

    # Compter le nombre de recettes par contributeur
    contributor_counts = df.groupby('contributor_id')['recipe_id'].count()

    # Trier par ordre décroissant et sélectionner les top N contributeurs
    top_contributors = contributor_counts.sort_values(ascending=False).head(top_n)

    # Réinitialiser l'index pour un DataFrame structuré
    result = top_contributors.reset_index()
    result.columns = ['contributor_id', 'num_recipes']

    return result


def get_top_ingredients2(df, df_ingr_map, excluded_ingredients=None, top_n=10):
    """Finds the most frequently used ingredients, excluding common ones.

    Args:
        merged_df (pd.DataFrame): DataFrame with recipe data, including 'recipe_id' and 'ingredient_ids'.
        df_ingr_map (pd.DataFrame): DataFrame mapping ingredient IDs ('id') to their names ('replaced').
        excluded_ingredients (set, optional): Ingredients to exclude. Defaults to common ingredients.
        top_n (int, optional): Number of top ingredients to return. Defaults to 10.

    Returns:
        pd.Series: Top `top_n` ingredients and their counts.
    """

    # Create a dictionary to map ingredient IDs to their simplified names
    ingr_map = df_ingr_map.set_index('id')['replaced'].to_dict()




    # Function to map ingredient IDs to simplified ingredient names
    def map_ingredient_ids(ids, ingr_map):
        if pd.isna(ids):
            return []
        try:
            return [ingr_map.get(int(ingr_id), 'Unknown') for ingr_id in ast.literal_eval(ids)]
        except (ValueError, SyntaxError):
            return []

    # Apply mapping to unique recipes
    df['mapped_ingredients'] = df['ingredient_ids'].apply(
        lambda x: map_ingredient_ids(x, ingr_map)
    )

    # Default list of ingredients to exclude
    if excluded_ingredients is None:
        excluded_ingredients = {'black pepper', 'vegetable oil', 'salt', 'pepper', 'olive oil', 'oil',
                                'butter', 'water', 'sugar', 'flour', 'brown sugar', 'salt and pepper',
                                'scallion', 'baking powder', 'garlic', 'flmy', 'garlic clove',
                                'all-purpose flmy', 'baking soda','ice cube'}

    # Filter/count occurrences of ingredients
    filtered_ingredient_counts = (
        df['mapped_ingredients']
        .explode()
        # Exclude common ingredients
        .loc[lambda x: ~x.isin(excluded_ingredients)]
        .value_counts()
        .head(top_n)
    )

    return filtered_ingredient_counts

def trendy_ingredients_by_seasons(df,ingr_map):
    """
    This function create a dataframe for each seasons and returns the top 200 ingredients used

    Args:
        df (dataframe): dataframe cleaned 
        ingr_map (dataFrame): dataFrame mapping ingredient IDs ('id') to their names ('replaced')

    Returns:
        winter_ingr,spring_ingr,summer_ingr,autumn_ingr (pd.series) : four pd.series with the top 200 ingredients used
    """

    # Dictionary mapping seasons to their corresponding months
    dico_season_months={'winter':['01','02','03'],'spring':['04','05','06'],'summer':['07','08','09'],'autumn':['10','11','12']}

    # Initialize empty dataFrames for each season
    winter=pd.DataFrame()
    spring=pd.DataFrame()
    summer=pd.DataFrame()
    autumn=pd.DataFrame()

    # Iterate over each season in the dictionary and concatenate rows where the 'month_date' matches the season months
    for i in dico_season_months.keys():
        if i == 'winter':
            for e in dico_season_months[i]:
                winter = pd.concat([winter, df[df['month_date'] == e]])
        if i == 'spring':
            for e in dico_season_months[i]:
                spring = pd.concat([spring, df[df['month_date'] == e]])
        if i == 'summer':
            for e in dico_season_months[i]:
                summer = pd.concat([summer, df[df['month_date'] == e]])
        if i == 'autumn':
            for e in dico_season_months[i]:
                autumn = pd.concat([autumn, df[df['month_date'] == e]])

    # Get the top 200 ingredients for each season
    winter_ingr=get_top_ingredients(winter, ingr_map, excluded_ingredients=None, top_n=200)
    spring_ingr=get_top_ingredients(spring, ingr_map, excluded_ingredients=None, top_n=200)
    summer_ingr=get_top_ingredients(summer, ingr_map, excluded_ingredients=None, top_n=200)
    autumn_ingr=get_top_ingredients(autumn, ingr_map, excluded_ingredients=None, top_n=200)

    return winter_ingr,spring_ingr,summer_ingr,autumn_ingr

def unique_ingr(winter_ingr,spring_ingr,summer_ingr,autumn_ingr):
    """
    This function return the unique ingredients used during each season by comparing all the ingredients used in
    one season to all the other seasons. 

    Args:
        winter_ingr (pd.series): ingredients used during winter
        spring_ingr (pd.series): ingredients used during spring
        summer_ingr (pd.series): ingredients used during summer
        autumn_ingr (pd.series): ingredients used during autumn

    Returns:
        winter_unique,spring_unique,summer_unique,autumn_unique (list): return a list for each season of unique ingredients 
    """

    # Initialize empty lists to store unique ingredient for each season
    winter_unique=[]
    spring_unique=[]
    summer_unique=[]
    autumn_unique=[]

    # For each season, identify unique index 
    for i in winter_ingr.index:
        if i not in spring_ingr.index and i not in summer_ingr.index and i not in autumn_ingr.index : 
            winter_unique.append(i)
    for i in spring_ingr.index:
        if i not in winter_ingr.index and i not in summer_ingr.index and i not in autumn_ingr.index : 
            spring_unique.append(i)
    for i in summer_ingr.index:
        if i not in winter_ingr.index and i not in spring_ingr.index and i not in autumn_ingr.index : 
            summer_unique.append(i)
    for i in autumn_ingr.index:
        if i not in winter_ingr.index and i not in summer_ingr.index and i not in spring_ingr.index : 
            autumn_unique.append(i)

    # Return unique indices for each season as a list
    return winter_unique,spring_unique,summer_unique,autumn_unique
  
def add_season(df):
    """ Add a season column to the dataframe """
    def get_season(month):
        if month in ('12', '01', '02'):
            return 'winter'
        elif month in ('03', '04', '05'):
            return 'spring'
        elif month in ('06', '07', '08'):
            return 'summer'
        elif month in ('09', '10', '11'):
            return 'autumn'

    df['season'] = df['month_date'].map(get_season)
    return df


def count_recipes_season(df):
    """ Count recipes per season """
    if 'season' not in list(df.columns):
        df['season'] = add_season(df)

    # count recipes per season
    recipe_per_season = {'winter': len(df[df['season'] == 'winter']),
                         'spring': len(df[df['season'] == 'spring']),
                         'summer': len(df[df['season'] == 'summer']),
                         'autumn': len(df[df['season'] == 'autumn'])}

    return recipe_per_season

def user_recipes(merged_df, user_id):
    """Finds the recipes published by the user

    Args:
        merged_df (pd.DataFrame): DataFrame with recipe data, including 'recipe_id' and 'ingredient_ids'.
        user_id (int): Contributor id of the user

    Returns:
        pd.Series: Top `top_n` ingredients and their counts.
    """
    recipes_user_df = merged_df.loc[merged_df["contributor_id"] == user_id]

    return recipes_user_df 

def count_recipes_per_user(df):
    """
    Counts the number of unique recipes published by each contributor.

    Args:
        df (pd.DataFrame): DataFrame with recipe data, including 'recipe_id' and 'contributor_id'.

    Returns:
        pd.Series: A series with contributors as the index and their unique recipe counts as values.
    """
    # Compter le nombre de recettes uniques pour chaque contributeur
    return df.groupby('contributor_id')['recipe_id'].nunique()