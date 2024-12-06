"""Function used for statistics. 
"""
import ast
import pandas as pd

def count_contributors_by_recipe_range_with_bins(df):
    """
    Categorizes contributors based on the number of unique recipes they have contributed 
    and counts how many contributors fall into each category.

    Parameters:
    - df (pd.DataFrame): A DataFrame containing at least two columns: 
        'contributor_id' (unique identifier for contributors) 
        'recipe_id' (unique identifier for recipes).

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
    labels = ['1 recette', '2 à 5 recettes',
              '6 à 8 recettes', 'Plus de 10 recettes']

    # Découper en catégories
    binned_counts = pd.cut(recipe_counts, bins=bins, labels=labels, right=True)

    # Compter le nombre de contributeurs dans chaque bin
    contributor_counts_by_bin = binned_counts.value_counts().sort_index()

    return contributor_counts_by_bin


def top_contributors_by_commented_recipes(df, top_n=10):
    """
    Returns the top X contributors who have published the most unique recipes.

    Parameters:
    - df (pd.DataFrame): A DataFrame containing recipe data.
    - top_n (int): Number of top contributors to return.

    Returns:
    - pd.Series: The `top_n` contributors with the count of unique recipes they have published.
    """
    # Filtrer les recettes qui ont des commentaires
    commented_recipes = df.dropna(subset=['review'])

    # Compter le nombre de commentaires par recette, puis par contributeur
    comments_per_contributor = commented_recipes.groupby(
        'contributor_id')['recipe_id'].count().sort_values(ascending=False).head(top_n)

    return comments_per_contributor


def top_tags(df, top_n=20):
    """
    Ensures each recipe_id is unique and returns the most frequently used tags.

    Parameters:
    - df (pd.DataFrame): A DataFrame containing recipe data.
    - top_n (int): Number of most frequent tags to return.

    Returns:
    - pd.Series: The `top_n` most frequently used tags.

    Raises:
    - ValueError: If duplicate `recipe_id` entries are detected.
    """

    # Exploser les tags pour avoir des lignes individuelles
    tags_series = df['tags'].apply(eval).explode()

    # Compter les tags les plus fréquents
    top_tags_used = tags_series.value_counts().head(top_n)
    return top_tags_used


def top_tags_most_commented(df, top_recipes=20, top_n=10):
    """
    Returns the most frequently used tags among the top X most commented recipes.

    Parameters:
    - df (pd.DataFrame): A DataFrame containing recipe data.
    - top_recipes (int): Number of most commented recipes to consider.
    - top_n (int): Number of most frequent tags to return.

    Returns:
    - pd.Series: The `top_n` most frequently used tags.
    """

    # Supprimer les recettes sans commentaires
    commented_recipes = df.dropna(subset=['review'])

    # Identifier les recettes les plus commentées
    most_commented = commented_recipes['recipe_id'].value_counts().head(
        top_recipes).index

    # Filtrer pour ces recettes
    filtered_df = df[df['recipe_id'].isin(most_commented)]

    # Exploser les tags et compter
    tags_series = filtered_df['tags'].apply(eval).explode()
    top_tags_commented = tags_series.value_counts().head(top_n)
    return top_tags_commented


def top_contributors_by_recipes(df, top_n=10):
    """
    Identifies the top contributors based on the number of unique recipes they have published.

    Args:
        df (pd.DataFrame): DataFrame containing recipe data with at least the following columns:
            - 'contributor_id': Unique identifier for contributors.
            - 'recipe_id': Unique identifier for recipes.
        top_n (int, optional): Number of top contributors to return. Defaults to 10.

    Returns:
        pd.Series: A series with the top `top_n` contributors as the index and the count of unique recipes 
                   they have published as the values, sorted in descending order. Returns None if required 
                   columns are missing.
    """
    if 'contributor_id' not in df or 'recipe_id' not in df:
        return None
    unique_recipes_df = df.drop_duplicates(subset='recipe_id')
    return unique_recipes_df['contributor_id'].value_counts().head(top_n)


def get_top_ingredients(merged_df, df_ingr_map, excluded_ingredients=None, top_n=10):
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

    # Remove duplicate recipes
    unique_recipes = merged_df.drop_duplicates(subset='recipe_id')

    # Function to map ingredient IDs to simplified ingredient names
    def map_ingredient_ids(ids, ingr_map):
        if pd.isna(ids):
            return []
        try:
            return [ingr_map.get(int(ingr_id), 'Unknown') for ingr_id in ast.literal_eval(ids)]
        except (ValueError, SyntaxError):
            return []

    # Apply mapping to unique recipes
    unique_recipes['mapped_ingredients'] = unique_recipes['ingredient_ids'].apply(
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
        unique_recipes['mapped_ingredients']
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


