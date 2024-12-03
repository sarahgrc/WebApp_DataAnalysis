# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 19:31:05 2024

@author: sarah
"""

from load_data.LoadData import DataFrameLoadder
import seaborn as sns
import matplotlib.pyplot as plt

df = DataFrameLoadder(path_raw_interaction='../data_files/RAW_interactions.csv',
                      path_raw_recipes='../data_files/RAW_recipes.csv',
                      pp_recipe='../data_files/PP_recipes.csv').load()


# Par période (mois) ⇒ regarder le nombre de recettes publié(KPI : best season to publish),
# dans ces mois la on regarde le temps et  // nb de recettes / saisons


# def count_recipes_seasons(df):


def add_season(df):
    """ Add a season column to the dataset """
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


def vis_count_per_season(df):
    """ """
    if 'season' not in list(df.columns):
        df['season'] = add_season(df)

    # count recipes per season
    recipe_per_season = {'winter': len(df[df['season'] == 'winter']),
                         'spring': len(df[df['season'] == 'spring']),
                         'summer': len(df[df['season'] == 'summer']),
                         'autumn': len(df[df['season'] == 'autumn'])}

    return recipe_per_season


def visualise_recipe_season(df):
    """ Visualise count per season"""
    dico_recpies_season = vis_count_per_season(df)
    print('----', dico_recpies_season)
    seasons = list(dico_recpies_season.keys())
    counts = list(dico_recpies_season.values())

    print(len(seasons))
    print(len(counts))

    sns.barplot(x=seasons, y=counts)
    plt.xlabel('season')
    plt.ylabel('count')
    plt.title('Recipes count per season')
    plt.show()


visualise_recipe_season(df)
