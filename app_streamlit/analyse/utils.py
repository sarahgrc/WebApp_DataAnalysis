"""functions used for statistics"""

import ast
import pandas as pd 

def metrics_main_contributor(df):
    """
    Calculate the total number of unique contributors and recipes in the dataset.

    Args:
        df (pd.DataFrame): DataFrame containing recipe data.

    Returns:
        tuple: Number of unique contributors and recipes.
    """
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
    Calculate the average and total number of comments per contributor.

    Args:
        df (pd.DataFrame): DataFrame containing 'contributor_id' and 'num_comments'.

    Returns:
        pd.DataFrame: DataFrame with 'contributor_id', 'avg_comments_per_recipe', and 'total_comments'.
    """
    if 'contributor_id' not in df.columns or 'num_comments' not in df.columns:
        raise ValueError("The DataFrame must contain 'contributor_id' and 'num_comments'.")

    df['contributor_id'] = df['contributor_id'].astype(str)

    stats = df.groupby('contributor_id')['num_comments'].agg(
        avg_comments_per_recipe='mean',
        total_comments='sum'
    ).reset_index()

    stats = stats.sort_values(by='avg_comments_per_recipe', ascending=False)
    return stats

def top_commented_recipes_by_contributors(df, top_contributors, max_recipes_per_contributor=5):
    """
    Extract top commented recipes for each contributor in the top contributors list.

    Args:
        df (pd.DataFrame): DataFrame containing recipe data.
        top_contributors (pd.DataFrame): DataFrame of top contributors.
        max_recipes_per_contributor (int): Maximum number of recipes per contributor.

    Returns:
        pd.DataFrame: DataFrame containing contributor IDs, recipe IDs, names, and number of comments.
    """
    required_columns = {'contributor_id', 'recipe_id', 'name', 'num_comments'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"The DataFrame must contain columns: {required_columns}.")

    df['contributor_id'] = df['contributor_id'].astype(str)
    top_contributors['contributor_id'] = top_contributors['contributor_id'].astype(str)

    filtered_df = df[df['contributor_id'].isin(top_contributors['contributor_id'])]
    filtered_df = filtered_df.sort_values(by='num_comments', ascending=False)


    top_recipes = (
        filtered_df.groupby('contributor_id')
        .head(max_recipes_per_contributor)
        .reset_index(drop=True)
    )

    return top_recipes[['contributor_id', 'recipe_id', 'name', 'num_comments']]

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

def count_contributors_by_recipe_range_with_bins(df):
    """
    Categorize contributors based on the number of unique recipes they contributed.

    Args:
        df (pd.DataFrame): DataFrame containing 'recipe_id' and 'contributor_id'.

    Returns:
        pd.Series: Series with recipe range categories as index and contributor counts as values.
    """
    recipe_counts = df.groupby('contributor_id')['recipe_id'].nunique()
    bins = [0, 1, 5, 8, float('inf')]
    labels = ['1 recipe', '2-5 recipes', '6-8 recipes', '> 8 recipes']

    binned_counts = pd.cut(recipe_counts, bins=bins, labels=labels, right=True)
    return binned_counts.value_counts().sort_index()

def top_commented_recipes(df, top_n=10):
    """
    Extract the top N recipes with the highest number of comments.

    Args:
        df (pd.DataFrame): DataFrame containing recipe data.
        top_n (int): Number of top recipes to return.

    Returns:
        pd.DataFrame: DataFrame containing top N recipes.
    """
    return df.sort_values(by='num_comments', ascending=False).head(top_n)[
        ['contributor_id', 'recipe_id', 'num_comments', 'name']
    ]

def get_top_tags(df, most_commented=False, top_recipes=20, top_n=10):
    """
    Retrieve the most frequently used tags.

    Args:
        df (pd.DataFrame): DataFrame containing recipe data.
        most_commented (bool): Whether to filter by the most commented recipes.
        top_recipes (int): Number of top recipes to consider if most_commented is True.
        top_n (int): Number of tags to return.

    Returns:
        pd.Series: Top N most frequently used tags.
    """
    if most_commented:
        most_commented_df = df.sort_values(by='num_comments', ascending=False).head(top_recipes)
        filtered_df = df[df['recipe_id'].isin(most_commented_df['recipe_id'])]
    else:
        filtered_df = df

    tags_series = filtered_df['tags'].apply(eval).explode()
    return tags_series.value_counts().head(top_n)

def get_top_ingredients2(df, df_ingr_map, excluded_ingredients=None, top_n=10):
    """
    Find the most frequently used ingredients, excluding common ones.

    Args:
        df (pd.DataFrame): DataFrame with recipe data.
        df_ingr_map (pd.DataFrame): DataFrame mapping ingredient IDs to their names.
        excluded_ingredients (set, optional): Ingredients to exclude.
        top_n (int): Number of top ingredients to return.

    Returns:
        pd.Series: Top N ingredients and their counts.
    """
    ingr_map = df_ingr_map.set_index('id')['replaced'].to_dict()

    def map_ingredient_ids(ids):
        if pd.isna(ids):
            return []
        try:
            return [ingr_map.get(int(ingr_id), 'Unknown') for ingr_id in ast.literal_eval(ids)]
        except (ValueError, SyntaxError):
            return []

    df['mapped_ingredients'] = df['ingredient_ids'].apply(map_ingredient_ids)

    if excluded_ingredients is None:
        excluded_ingredients = {
            'black pepper', 'vegetable oil', 'salt', 'pepper', 'olive oil',
            'butter', 'water', 'sugar', 'flour', 'brown sugar',
        }

    filtered_ingredients = (
        df['mapped_ingredients']
        .explode()
        .loc[lambda x: ~x.isin(excluded_ingredients)]
        .value_counts()
        .head(top_n)
    )


    return filtered_ingredients
"""
def count_recipes_season(df):
    
    Count recipes per season.

    return filtered_ingredient_counts
"""
def trendy_ingredients_by_seasons(df,ingr_map,top_n):
    """
    This function create a dataframe for each seasons and returns the top 200 ingredients used

    Args:
        df (dataframe): dataframe cleaned 
        ingr_map (dataFrame): dataFrame mapping ingredient IDs ('id') to their names ('replaced')
        top_n (int, optional): number of top ingredients to return. Defaults to 200.
    
    Returns:
        winter_ingr,spring_ingr,summer_ingr,autumn_ingr (pd.series) : four pd.series with the top 200 ingredients used
    """
    # Create dataFrames for each season
    winter= df[df['season']=='winter']
    spring=df[df['season']=='spring']
    summer=df[df['season']=='summer']
    autumn=df[df['season']=='autumn']

    # Get the top 200 ingredients for each season
    winter_ingr=get_top_ingredients2(winter, ingr_map, excluded_ingredients=None, top_n=top_n)
    spring_ingr=get_top_ingredients2(spring, ingr_map, excluded_ingredients=None, top_n=top_n)
    summer_ingr=get_top_ingredients2(summer, ingr_map, excluded_ingredients=None, top_n=top_n)
    autumn_ingr=get_top_ingredients2(autumn, ingr_map, excluded_ingredients=None, top_n=top_n)

    return winter_ingr,spring_ingr,summer_ingr,autumn_ingr

def unique_ingr(df,ingr_map,top_n=200):
    """
    This function return the unique ingredients used during each season by comparing all the ingredients used in
    one season to all the other seasons. 

    Args:
        df (dataframe): dataframe cleaned 
        ingr_map (dataFrame): dataFrame mapping ingredient IDs ('id') to their names ('replaced')
        top_n (int, optional): number of top ingredients to return. Defaults to 200.

    Returns:
        winter_unique,spring_unique,summer_unique,autumn_unique (list): return a list for each season of unique ingredients 
    """

    winter_ingr,spring_ingr,summer_ingr,autumn_ingr=trendy_ingredients_by_seasons(df,ingr_map,top_n)
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
  
def count_recipes_season(df):
    """ Count recipes per season """
    # count recipes per season
    recipe_per_season = {'winter': len(df[df['season'] == 'winter']),
                         'spring': len(df[df['season'] == 'spring']),
                         'summer': len(df[df['season'] == 'summer']),
                         'autumn': len(df[df['season'] == 'autumn'])}

    return recipe_per_season

def user_recipes(merged_df, user_id):
    """Finds the recipes published by the user


    Args:
        df (pd.DataFrame): DataFrame with recipe data and a 'season' column.

    Returns:
        dict: Recipe counts per season.
    """
    recipes_user_df = merged_df.loc[merged_df["contributor_id"] == user_id]
    return recipes_user_df 


def calculate_negative_points_nutri_score(row):
    """
    Calculate the negative points that will lower the Nutri-Score based on 
    the levels of certain nutrients: calories, sugar, saturated fat, and sodium.

    Args:
        row (dict): row from a DataFrame representing nutrition of the recipe.

    Returns:
        int: The total negative points calculated based on the thresholds for the given nutrients.
    """
    # Calories
    if row["Calories"] <= 335: calories_points = 0
    elif row["Calories"] <= 670: calories_points = 1
    elif row["Calories"] <= 1005: calories_points = 2
    elif row["Calories"] <= 1340: calories_points = 3
    elif row["Calories"] <= 1675: calories_points = 4
    elif row["Calories"] <= 2010: calories_points = 5
    elif row["Calories"] <= 2345: calories_points = 6
    elif row["Calories"] <= 2680: calories_points = 7
    elif row["Calories"] <= 3015: calories_points = 8
    elif row["Calories"] <= 3350: calories_points = 9
    else: calories_points = 10

    # Sucres
    if row["Sugar"] <= 4.5: sugar_points = 0
    elif row["Sugar"] <= 9: sugar_points = 1
    elif row["Sugar"] <= 13.5: sugar_points = 2
    elif row["Sugar"] <= 18: sugar_points = 3
    elif row["Sugar"] <= 22.5: sugar_points = 4
    elif row["Sugar"] <= 27: sugar_points = 5
    elif row["Sugar"] <= 31: sugar_points = 6
    elif row["Sugar"] <= 36: sugar_points = 7
    elif row["Sugar"] <= 40: sugar_points = 8
    elif row["Sugar"] <= 45: sugar_points = 9
    else: sugar_points = 10

    # Graisses saturées
    if row["Saturated Fat"] <= 1: fat_points = 0
    elif row["Saturated Fat"] <= 2: fat_points = 1
    elif row["Saturated Fat"] <= 3: fat_points = 2
    elif row["Saturated Fat"] <= 4: fat_points = 3
    elif row["Saturated Fat"] <= 5: fat_points = 4
    elif row["Saturated Fat"] <= 6: fat_points = 5
    elif row["Saturated Fat"] <= 7: fat_points = 6
    elif row["Saturated Fat"] <= 8: fat_points = 7
    elif row["Saturated Fat"] <= 9: fat_points = 8
    elif row["Saturated Fat"] <= 10: fat_points = 9
    else: fat_points = 10

    # Sodium
    if row["Sodium"] <= 90: sodium_points = 0
    elif row["Sodium"] <= 180: sodium_points = 1
    elif row["Sodium"] <= 270: sodium_points = 2
    elif row["Sodium"] <= 360: sodium_points = 3
    elif row["Sodium"] <= 450: sodium_points = 4
    elif row["Sodium"] <= 540: sodium_points = 5
    elif row["Sodium"] <= 630: sodium_points = 6
    elif row["Sodium"] <= 720: sodium_points = 7
    elif row["Sodium"] <= 810: sodium_points = 8
    elif row["Sodium"] <= 900: sodium_points = 9
    else: sodium_points = 10

    return calories_points + sugar_points + fat_points + sodium_points

def calculate_positive_points_nutri_score(row):
    """
    Calculate the positive points that will improve the Nutri-Score based on 
    the level of protein in the food.

    Args:
        row (dict): row from a DataFrame representing a food item. 

    Returns:
        int: The total positive points calculated based on the protein thresholds.
    """
    if row["Protein"] <= 1.6: protein_points = 0
    elif row["Protein"] <= 3.2: protein_points = 1
    elif row["Protein"] <= 4.8: protein_points = 2
    elif row["Protein"] <= 6.4: protein_points = 3
    elif row["Protein"] <= 8: protein_points = 4
    else: protein_points = 5

    return protein_points

def nutri_score(df):
    """
    Calculate the overall Nutri-Score (A to E) for a food item by considering both 
    negative and positive points. 

    Args:
        df : DataFrame representing a food item. 
                    It should include keys required for both negative and positive point 
                    calculations: "Calories", "Sugar", "Saturated Fat", "Sodium", and "Protein".

    Returns:
        str: The Nutri-Score grade (A, B, C, D, or E) based on the calculated score.
    """
    negative_points = calculate_negative_points_nutri_score(df)
    positive_points = calculate_positive_points_nutri_score(df)
    score = negative_points - positive_points

    # Conversion Nutri-Score
    if score <= -1:
        return "A"
    elif 0 <= score <= 2:
        return "B"
    elif 3 <= score <= 10:
        return "C"
    elif 11 <= score <= 18:
        return "D"
    else:
        return "E"
    

def top_recipes_user(df):
    """
    Returns the top 5 recipes with the most comments from a specific user.

    Args:
        df : pandas.DataFrame
            DataFrame with these columns:
            - 'user_id': user IDs
            - 'name': recipe names.

    Returns:
        pandas.DataFrame
            A DataFrame with:
            - 'Recipe': recipe names
            - 'Number of comments': count of comments per recipe.
    """
    top_user_recipe =  df['name'].value_counts().head(5)
    top_user_recipe_df = top_user_recipe.reset_index()
    top_user_recipe_df.columns = ['Recipe', 'Number of comments']
    
    return top_user_recipe_df


def top_recipes(df):
    """
    Returns the top 5 recipes with the most comments.

    Args:
        df : pandas.DataFrame
            DataFrame with all the preprocessed data

    Returns:
        pandas.DataFrame
    """
    # Top 5 commented recipes
    top_recipe = df['name'].value_counts().head(5)
    # Convert Series to DataFrame
    top_recipe_df = top_recipe.reset_index()
    top_recipe_df.columns = ['Recipe', 'Number of comments']
    # Mean rating for each recipe 
    mean_rating_df = (
        df.groupby('name')['rating']
        .mean()
        .reset_index()
        .rename(columns={'rating': 'Mean Rating'})
    )
    # Add the rating mean to the table 
    top_recipe_df = top_recipe_df.merge(mean_rating_df, left_on='Recipe', right_on='name', how='left')
    # remove col 'name' cause redondance
    top_recipe_df.drop(columns=['name'], inplace=True)

    return top_recipe_df

