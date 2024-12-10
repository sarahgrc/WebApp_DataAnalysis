"""functions used for statistics"""

import ast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import logging


logging.basicConfig(
    filename='logging/debug.log',
    level=logging.DEBUG,
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def metrics_main_contributor(df):
    """
    Calculate the total number of unique contributors and recipes in the dataset.

    Args:
        df (pd.DataFrame): DataFrame containing recipe data.

    Returns:
        tuple: Number of unique contributors and recipes.
    """
    logging.debug("Calculating number of unique contributors and recipes.")
    num_contributors = df['contributor_id'].nunique()
    num_recipes = df['recipe_id'].nunique()
    logging.info(f"Number of contributors: {num_contributors}, Number of recipes: {num_recipes}")
    return num_contributors, num_recipes


def average_and_total_comments_per_contributor(df):
    """
    Calculates the average number of comments per recipe and the total number of comments for each contributor.

    Arg:
        df (pd.DataFrame): A DataFrame containing recipe data, including 'contributor_id' and 'num_comments'.

    Returns:
        df (pd.DataFrame): A DataFrame with 'contributor_id', 'avg_comments_per_recipe', and 'total_comments', where contributor_id is treated as a category.
    """

    # Vérifier que les colonnes nécessaires existent
    logging.debug("Starting calculation of average and total comments per contributor.")
    if 'contributor_id' not in df.columns or 'num_comments' not in df.columns:
        logging.error("Required columns 'contributor_id' and 'num_comments' are missing.")

    # Convertir contributor_id en chaîne
    logging.debug("Converting 'contributor_id' to string type.")
    df['contributor_id'] = df['contributor_id'].astype(str)

    # Calculer la moyenne des commentaires et le total des commentaires par contributeur
    logging.debug("Grouping data by 'contributor_id' and calculating statistics.")
    stats = df.groupby('contributor_id')['num_comments'].agg(
        avg_comments_per_recipe='mean',  # Moyenne des commentaires
        total_comments='sum'            # Total des commentaires
    ).reset_index()

    # Renommer les colonnes pour plus de clarté
    stats.columns = ['contributor_id', 'avg_comments_per_recipe', 'total_comments']

    # Trier par moyenne décroissante
    stats = stats.sort_values(by='avg_comments_per_recipe', ascending=False)
    logging.info("Successfully calculated average and total comments per contributor.")
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
    logging.debug("Extracting top commented recipes by contributors.")
    if not {'contributor_id', 'recipe_id', 'name', 'num_comments'}.issubset(df.columns):
        logging.error("The DataFrame must contain 'contributor_id', 'recipe_id', 'name', and 'num_comments'.")

    # Convertir contributor_id en chaîne dans les deux DataFrames
    logging.debug("Filtering DataFrame to include only the top contributors.")
    df['contributor_id'] = df['contributor_id'].astype(str)
    top_contributors['contributor_id'] = top_contributors['contributor_id'].astype(str)

    # Filtrer les recettes appartenant aux top contributeurs
    filtered_df = df[df['contributor_id'].isin(top_contributors['contributor_id'])]
    
    # Trier les recettes par nombre de commentaires
    logging.debug("Sorting recipes by number of comments.")
    filtered_df = filtered_df.sort_values(by='num_comments', ascending=False)
    
    # Limiter le nombre de recettes par contributeur
    logging.debug("Limiting the number of recipes per contributor.")
    top_recipes = (
        filtered_df.groupby('contributor_id')
        .head(max_recipes_per_contributor)
        .reset_index(drop=True)
    )
    
    # Sélectionner les colonnes pertinentes
    logging.info(f"Extracted top commented recipes for {len(top_recipes)} records.")
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
        logging.error("The DataFrame must contain 'contributor_id' and 'num_comments'.")

    df['contributor_id'] = df['contributor_id'].astype(str)

    logging.debug("Calculating average and total comments per contributor.")
    stats = df.groupby('contributor_id')['num_comments'].agg(
        avg_comments_per_recipe='mean',
        total_comments='sum'
    ).reset_index()

    logging.info(f"Calculated stats for {len(stats)} contributors.")
    stats = stats.sort_values(by='avg_comments_per_recipe', ascending=False)
    logging.debug(f"Top contributors by average comments: {stats.head()}")
    return stats

def count_contributors_by_recipe_range_with_bins(df):
    """
    Categorize contributors based on the number of unique recipes they contributed.

    Args:
        df (pd.DataFrame): DataFrame containing 'recipe_id' and 'contributor_id'.

    Returns:
        pd.Series: Series with recipe range categories as index and contributor counts as values.
    """
    if 'recipe_id' not in df.columns or 'contributor_id' not in df.columns:
        logging.error("The required columns 'recipe_id' and 'contributor_id' are missing.")

    recipe_counts = df.groupby('contributor_id')['recipe_id'].nunique()
    logging.info(f"Calculated unique recipe counts for {len(recipe_counts)} contributors.")
    bins = [0, 1, 5, 8, float('inf')]
    labels = ['1 recipe', '2-5 recipes', '6-8 recipes', '> 8 recipes']
    logging.debug(f"Defining bins: {bins} and labels: {labels}.")

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
    logging.debug("Starting the function to extract top commented recipes.")
    
    if 'num_comments' not in df.columns :
        logging.error("The DataFrame is missing required columns: 'num_comments'.")
    
    logging.debug(f"Sorting the DataFrame by 'num_comments' to find top {top_n} recipes.")
    top_recipes = df.sort_values(by='num_comments', ascending=False).head(top_n)[
        ['contributor_id', 'recipe_id', 'num_comments', 'name']
    ]
    
    logging.info(f"Top {top_n} recipes extracted successfully.")
    logging.debug(f"Top recipes:\n{top_recipes}")

    return top_recipes

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

    # Parse 'tags' strings into lists
    def parse_tags(value):
        if isinstance(value, str):
            # Remove brackets and split by commas
            return [tag.strip(" '\"") for tag in value.strip('[]').split(',')]
        return []

    # Apply parsing, then explode and count occurrences
    tags_series = filtered_df['tags'].apply(parse_tags).explode()
    return tags_series.value_counts().head(top_n)


def get_top_ingredients2(df, df_ingr_map, excluded_ingredients=None, top_n=10):
    ingr_map = df_ingr_map.set_index('id')['replaced'].to_dict()

    def parse_ingredient_ids(ids, ingr_map):
        if isinstance(ids, str):
            ids = ids.strip('[]')
            try:
                logging.debug(f"Parsing ingredient IDs: {ids}")
                return [ingr_map.get(int(ingr.strip()), 'Unknown') for ingr in ids.split(',') if ingr.strip()]
            except ValueError:
                logging.error(f"ValueError while parsing ingredient IDs: {ids}")
                return []
        return []
    
    df['mapped_ingredients'] = df['ingredient_ids'].apply(lambda ids: parse_ingredient_ids(ids, ingr_map))
    if excluded_ingredients is None:
        excluded_ingredients = {
            'black pepper', 'vegetable oil', 'salt', 'pepper', 'olive oil',
            'butter', 'water', 'sugar', 'flour', 'brown sugar',
        }
        logging.debug(f"Using default excluded ingredients: {excluded_ingredients}")

    filtered_ingredients = (df['mapped_ingredients']
        .explode()
        .loc[lambda x: ~x.isin(excluded_ingredients)]
        .value_counts()
        .head(top_n)
    )
    
    logging.info(f"Top {top_n} ingredients extracted successfully.")
    logging.debug(f"Top ingredients:\n{filtered_ingredients}")
    return filtered_ingredients


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
    logging.debug(f"Starting trendy_ingredients_by_seasons with top_n={top_n}")
    # Create dataFrames for each season
    winter= df[df['season']=='winter']
    spring=df[df['season']=='spring']
    summer=df[df['season']=='summer']
    autumn=df[df['season']=='autumn']
    logging.info("Dataframes for each season created successfully.")

    # Get the top 200 ingredients for each season
    winter_ingr=get_top_ingredients2(winter, ingr_map, excluded_ingredients=None, top_n=top_n)
    spring_ingr=get_top_ingredients2(spring, ingr_map, excluded_ingredients=None, top_n=top_n)
    summer_ingr=get_top_ingredients2(summer, ingr_map, excluded_ingredients=None, top_n=top_n)
    autumn_ingr=get_top_ingredients2(autumn, ingr_map, excluded_ingredients=None, top_n=top_n)
    logging.info(f"Top {top_n} ingredients extracted for each season.")
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
    logging.debug(f"Winter unique ingredients: {len(winter_unique)}")

    for i in spring_ingr.index:
        if i not in winter_ingr.index and i not in summer_ingr.index and i not in autumn_ingr.index : 
            spring_unique.append(i)
    logging.debug(f"Spring unique ingredients: {len(spring_unique)}")

    for i in summer_ingr.index:
        if i not in winter_ingr.index and i not in spring_ingr.index and i not in autumn_ingr.index : 
            summer_unique.append(i)
    logging.debug(f"Summer unique ingredients: {len(summer_unique)}")

    for i in autumn_ingr.index:
        if i not in winter_ingr.index and i not in summer_ingr.index and i not in spring_ingr.index : 
            autumn_unique.append(i)
    logging.debug(f"Autumn unique ingredients: {len(autumn_unique)}")

    logging.info(f"Unique ingredients identified for each season: Winter={len(winter_unique)}, Spring={len(spring_unique)}, Summer={len(summer_unique)}, Autumn={len(autumn_unique)}")
    # Return unique indices for each season as a list
    return winter_unique,spring_unique,summer_unique,autumn_unique
  
def count_recipes_season(df):
    """ Count recipes per season """
    # count recipes per season
    recipe_per_season = {'winter': len(df[df['season'] == 'winter']),
                         'spring': len(df[df['season'] == 'spring']),
                         'summer': len(df[df['season'] == 'summer']),
                         'autumn': len(df[df['season'] == 'autumn'])}
    logging.debug(f"Recipe count per season: {recipe_per_season}")
    return recipe_per_season

def user_recipes(merged_df, user_id):
    """Finds the recipes published by the user


    Args:
        df (pd.DataFrame): DataFrame with recipe data and a 'season' column.

    Returns:
        dict: Recipe counts per season.
    """

    recipes_user_df = merged_df.loc[merged_df["contributor_id"] == user_id]
    logging.debug(f"Number of recipes found for user_id {user_id}: {len(recipes_user_df)}")
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
    logging.debug(f"Calculated positive points based on Protein value {row['Protein']}: {protein_points}")
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
    logging.debug(f"Negative points: {negative_points}, Positive points: {positive_points}")
    score = negative_points - positive_points
    logging.debug(f"Nutri-Score calculated score: {score}")
    # Conversion Nutri-Score
    if score <= -1:
        grade = "A"
    elif 0 <= score <= 2:
        grade = "B"
    elif 3 <= score <= 10:
        grade = "C"
    elif 11 <= score <= 18:
        grade = "D"
    else:
        grade = "E"

    # Log the final grade
    logging.debug(f"Nutri-Score grade: {grade}")

    return grade
    
def top_recipes_user(df):
    """
    Returns the top 5 recipes with the most comments from a specific user.

    Args:
        df : pandas.DataFrame
            DataFrame with these columns:
            - 'name': recipe names.
            - 'avg_reviews': average rating.
            - 'num_comments': number of comments.

    Returns:
        pandas.DataFrame
            A DataFrame with:
            - 'Recipe': recipe names.
            - 'Number of comments': count of comments per recipe.
            - 'Average Rating': average rating for each recipe.
    """
    # Filtrer les recettes valides
    filtered_df = df[df['name'].notna()]
    logging.debug(f"Filtered data (recipes with valid names):\n{filtered_df.head()}")
    # Sélectionner les colonnes nécessaires et trier
    top_user_recipe = filtered_df[['name', 'num_comments', 'avg_reviews']].sort_values(
        by=['num_comments', 'avg_reviews'], ascending=[False, False]
    ).head(5)
    logging.debug(f"Top 5 recipes based on comments and ratings:\n{top_user_recipe}")
    # Renommer les colonnes pour une meilleure lisibilité
    top_user_recipe = top_user_recipe.rename(
        columns={'name': 'Recipe', 'num_comments': 'Number of comments', 'avg_reviews': 'Average Rating'}
    )

    return top_user_recipe



def top_recipes(df):
    """
    Returns the top 5 recipes with the most comments.

    Args:
        df pd.DataFrame : DataFrame with all the preprocessed data

    Returns:
        pd.DataFrame
    """

    logging.debug("Starting to find the top 5 recipes with the most comments.")
    logging.debug(f"Initial DataFrame:\n{df.head()}")

    filtered_df = df[df['name'].notna()]
    assert filtered_df['name'].isna().sum() == 0, "Filtered DataFrame still contains NaN in 'name'"
    logging.debug(f"Filtered DataFrame (no NaN in 'name'):\n{filtered_df.head()}")
    # Top 5 commented recipes
    top_recipe_df = filtered_df[['name', 'num_comments', 'avg_reviews']].sort_values(
        by='num_comments', ascending=False
    ).head(5)
    logging.debug(f"Top 5 recipes based on number of comments:\n{top_recipe_df}")
    top_recipe_df = top_recipe_df.rename(
        columns={'name': 'Recipe', 'num_comments': 'Number of comments', 'avg_reviews': 'Avg reviews'}
    )
    logging.debug(f"Top 5 recipes with renamed columns:\n{top_recipe_df}")
    return top_recipe_df


def cat_minutes(df):
    """
    Transform columns minutes in categorical values

    Args:
        df : (pd.DataFrame) : DataFrame containnning 'minutes' column

    Returns:
        cat_minutes : pd.Series : 'minutes' column transformed in categorical values

    """
    cat_minutes = ['less_15min' if 0 <= x <= 15 else
                   '15_30min' if 15 < x <= 30 else
                   '30min_1h' if 30 < x <= 60 else
                   '1h_2h' if 60 < x <= 120 else
                   '2h_3h' if 120 < x <= 180 else
                   '3h_4h' if 180 < x < 240 else
                   '4h_more'
                   for x in df['minutes']]

    return cat_minutes


def best_recipe_filter_time(df, time_r, nb_show):
    """
    Get information about the best recipes (ranking-higher comments) filtered on time of preparation

    args:
        df : pd.DataFrame : dataframe containing columns 'minutes','name', 'n_steps', 'num_comments', 'ingredients','avg_reviews'
        time_r : str : time of preparation (categorie) we want to filter results on 
        nb_show : int : number of recipes to show

    Returns:
        result : pd.DataFrame : recipes info that have the best ranking + higher comment filtered on time_r

    """
    logging.debug("Starting best_recipe_filter_time function.")
    logging.debug(f"Received time_r: {time_r}, nb_show: {nb_show}")

    list_cat_time = ['less_15min', '15_30min',
                     '30min_1h', '1h_2h', '2h_3h', '3h_4h', '4h_more']
    
    if time_r not in list_cat_time or not nb_show in [1, 2, 3, 4, 5, 10]:
        error_msg = f"** ERROR ** time_r should be in {list_cat_time} - got: {time_r}, and nb_show in [1, 2, 3, 4, 5, 10] - got: {nb_show}"
        logging.error(error_msg)
    
    if 'minutes_tr' not in df.columns : 
        logging.debug("Creating 'minutes_tr' column using 'cat_minutes'.")
        df['minutes_tr'] = cat_minutes(df)

    df = df[df['minutes_tr'] == time_r]

    result = df[df['avg_reviews'] == 5][['name', 'n_steps', 'num_comments', 'ingredients','avg_reviews']]
    logging.debug(f"Filtered recipes with perfect ratings (5): {len(result)} records.")
    result = result.sort_values(by='num_comments', ascending=False).head(nb_show)
    logging.debug(f"Sorted and selected top {nb_show} recipes with highest comments.")
    logging.debug(f"Returning result with {len(result)} records.")
    return result

def get_insight_low_ranking(df):
    """
    get insight of number of recipes per time of preparation for all the recipes and for low ranking recpies
    
    args :
        df : (pd.DataFrame) : DataFrame 

    Returns : 
        df_low_count : (pd.DataFrame) filter on low ranking
        df_high_count : (pd.DataFrame) filter on high ranking

    """
    logging.debug(f"Initial DataFrame shape: {df.shape}")

    if 'minutes_tr' not in df.columns : 
        logging.debug("Creating 'minutes_tr' column using 'cat_minutes'.")
        df['minutes_tr'] = cat_minutes(df)

    # filter low ranking - insight on time preparation
    df_low_rating = df[df['avg_reviews'].isin([1, 2])]
    logging.debug(f"Filtered low-ranking recipes: {len(df_low_rating)} records.")

    df_low_count = df_low_rating.groupby(
        ['minutes_tr']).size().reset_index(name='count')
    l_low = np.sum(df_low_count['count'])
    df_low_count['count'] = np.round(df_low_count['count']*100/l_low, 2)
    
    # filter high ranking - insight on time preparation
    df_high_count = df.groupby(['minutes_tr']).size().reset_index(name='count')    
    l_all = np.sum(df_high_count['count'])
    df_high_count['count'] = np.round(df_high_count['count']*100/l_all, 2)
    logging.debug("Returning df_low_count and df_high_count.")
    return df_low_count, df_high_count


def visualise_recipe_season(df):
    """Visualise count per season with low and high rankings."""
    
    # Filter for high and low rankings
    df_high = df[df['avg_reviews'].isin([4, 5])]
    df_low = df[df['avg_reviews'].isin([1, 2, 3])]
    logging.debug(f"Number of high-ranking recipes: {len(df_high)}")
    logging.debug(f"Number of low-ranking recipes: {len(df_low)}")

    # Count recipes per season
    count_data_high = df_high.groupby(['season']).size().reset_index(name='count')
    count_data_low = df_low.groupby(['season']).size().reset_index(name='count')
    
    # Create the plot
    fig, ax = plt.subplots()
    sns.barplot(x='season', y='count', data=count_data_low, color='blue', label='Low ranking', ax=ax)
    sns.barplot(x='season', y='count', data=count_data_high, alpha=0.7, color='orange', label='High ranking', ax=ax)
    ax.set_xlabel('Season')
    ax.set_ylabel('Count')
    ax.set_title('Recipes count per season', weight='bold')
    ax.legend()
    
    logging.debug("Plot created successfully.")
    return fig

def visualise_low_rank_insight(df_low_count, df_high_count):
    """ Visualise low vs high rank recipes over time of preparation"""
    fig, ax = plt.subplots()
    sns.barplot(df_low_count, x='minutes_tr', y='count',
                label='low rating distribution', alpha=0.9, dodge=True)
    sns.barplot(df_high_count, x='minutes_tr',  y='count',
                label='all rating distribution', alpha=0.7, dodge=True)
    ax.set_xlabel('time of preparation')
    ax.set_ylabel('% of recipies')
    ax.set_title('Sum of recipies (in %) per time of  preparation ', weight='bold')
    ax.legend()
    return fig 
