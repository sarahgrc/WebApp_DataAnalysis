# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:24:19 2024

@author: Sarah
"""

from .preprocess.clean_dataframe import prepare_final_dataframe
from .preprocess.merging import dataframe_concat
import pandas as pd


class DataFrameLoadder():
    # FIXME : --> add upload csv files
    def __init__(self,  path_raw_interaction: str):
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
        
        self.raw_interaction = pd.read_csv(self.path_raw_interaction)
        self.df = self.raw_interaction

        return self.df
