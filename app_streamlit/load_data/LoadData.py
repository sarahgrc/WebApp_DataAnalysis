# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:24:19 2024

@author: Sarah
"""

from load_data.preprocess.clean_dataframe import prepare_final_dataframe
from load_data.preprocess.merging import dataframe_concat
import pandas as pd


class DataFrameLoadder():
    # FIXME : --> add upload csv files
    def __init__(self,  path_raw_interaction: str, path_raw_recipes: str, pp_recipe: str):
        """
        Dataset Loadder

            *** Will be further modify to automaticly download csv files ****

        Args:
            path_raw_interaction (str): path to raw_interaction.csv.
            path_raw_recipes (str): path to raw_recipies.csv.
            pp_recipe (TYPE): path_pp_recipe.csv.

        Returns:
            None.

        """
        self.path_raw_interaction = path_raw_interaction
        self.path_raw_recipes = path_raw_recipes
        self.path_pp_recipe = pp_recipe

    def __getitem__(self, df_name: str):
        if not isinstance(df_name, str):
            raise TypeError(
                f'--- TYPE ERROR --- : df_name should be str got instead {type(df_name)} ')
        if df_name not in ['raw_interaction', 'raw_recipes', 'pp_recipe']:
            raise ValueError(
                f"--- VALUE ERROR --- : df_name should be in ['raw_interaction', 'raw_recipes', 'pp_recipe'] ")

        else:
            return pd.read_csv(self.df_name)

    def load(self):
        try:
            self.raw_interaction = pd.read_csv(self.path_raw_interaction)
            self.raw_recipes = pd.read_csv(self.path_raw_recipes)
            self.pp_recipe = pd.read_csv(self.path_pp_recipe)
            self.df = prepare_final_dataframe(
                self.raw_interaction, self.raw_recipes, self.pp_recipe)
        except FileNotFoundError:
            print('--- FILE NOT FOUND --- check csv creation ')
        except Exception as e:
            print(' -- UNEXPECTED ERROR --- : ', e)

        return self.df
