# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 19:31:05 2024

@author: sarah
"""

from load_data.LoadData import DataFrameLoadder
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np




# def count_recipes_seasons(df):

# ============= deja dans le cleaning df 
def add_season(df):
    """ Add a season column to the dataset """
    def get_season(month):
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        elif month in [9, 10, 11]:
            return 'autumn'

    df['season'] = df['month'].map(get_season)
    return df


def visualise_recipe_season(df):
    """ Visualise count per season"""
    if 'season' not in list(df.columns):
        df = add_season(df)

    # count recipes per season
    count_data = df.groupby(['season']).size().reset_index(name='count')

    sns.set_palette('plasma')
    sns.barplot(x='season', y='count', data=count_data, color='lightblue')
    plt.xlabel('season')
    plt.ylabel('count')
    plt.title('Recipes count per season')
    plt.show()


# visualise_recipe_season(df)


#  |||| temps de cuisson commun ? que pour les ratting 0-1-2-3

def cat_minutes(df):
    cat_minutes = ['less_15min' if 0 <= x <= 15 else
                   '15_30min' if 15 < x <= 30 else
                   '30min_1h' if 30 < x <= 60 else
                   '1h_2h' if 60 < x <= 120 else
                   '2h_3h' if 120 < x <= 180 else
                   '3h_4h' if 180 < x < 240 else
                   '4h_more'
                   for x in df['minutes']]

    return cat_minutes


def get_insight_low_ranking(df):
    """
    get insight of number of recipes per time of preparation for all the recipes and for low ranking recpies
    
    Parameters
    ----------
    df : TYPE
        DESCRIPTION.

    Returns
    -------
    df_low_mintr : TYPE
        DESCRIPTION.
    df_mintr : TYPE
        DESCRIPTION.

    """
    if 'minutes_tr' not in df.columns : 
        df['minutes_tr'] = cat_minutes(df)

    # filter low ranking - insight on time preparation
    df_low_rating = df[df['avg_reviews'].isin([1, 2])]
    df_low_mintr = df_low_rating.groupby(
        ['minutes_tr']).size().reset_index(name='count')
    l_low = np.sum(df_low_mintr['count'])
    df_low_mintr['count'] = np.round(df_low_mintr['count']*100/l_low, 2)
    
    # for all recipes
    df_mintr = df.groupby(['minutes_tr']).size().reset_index(name='count')    
    l_all = np.sum(df_mintr['count'])
    df_mintr['count'] = np.round(df_mintr['count']*100/l_all, 2)
    return df_low_mintr, df_mintr
    


def visualise_low_rank_insight(df_low_index, df_index):
    plt.figure()
    # sns.set_palette('vibrant')
    sns.barplot(df_low_index, x='minutes_tr', y='count',
                label='low rating distribution', alpha=0.9, dodge=True)
    sns.barplot(df_index, x='minutes_tr',  y='count',
                label='all rating distribution', alpha=0.7, dodge=True)
    plt.xlabel('time of preparation')
    plt.ylabel('% of recipies')
    plt.legend()
    plt.title('Sum of recipies (in %) per time of  preparation ', weight='bold')
    plt.show()




def best_recipe_filter_time(df, time_r, nb_show):
    """ """
    list_cat_time = ['less_15min', '15_30min',
                     '30min_1h', '1h_2h', '2h_3h', '3h_4h', '4h_more']
    
    if time_r not in list_cat_time or not nb_show in [0, 1, 2, 3, 4, 5]:
        raise ValueError(f' ** ERROR ** time_r should be in {list_cat_time} -got : {
                         time_r} and  nb_show in [0,1,2,3] - got : {nb_show} ')

    df['minutes_tr'] = cat_minutes(df)
    df = df[df['minutes_tr'] == time_r]

    # FIXME : Add un si on trouve aucun -> regarde ratting a 4
    result = df[df['avg_reviews'] == 5][['name', 'n_steps', 'num_comments', 'ingredients','avg_reviews']]
    result = result.sort_values(by='num_comments', ascending=False).head(nb_show)
    
    return result


