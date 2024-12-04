import streamlit as st
import pandas as pd
import os
from load_data.LoadData import DataFrameLoadder


clean_df = DataFrameLoadder(path_raw_interaction='../data_files/RAW_interactions.csv',
                      path_raw_recipes='../data_files/RAW_recipes.csv',
                      pp_recipe='../data_files/PP_recipes.csv').load()

df_ingr_map=pd.read_pickle('../data_files/ingr_map.pkl')


def display_recipes_page():
    """
    Display the recipes page content.
    """

    # Get path of the images 
    current_dir = os.path.dirname(__file__)
    images_path = os.path.abspath(os.path.join(current_dir, "..", "images"))
    img_1_path =os.path.join(images_path, "raw-ingredient.png")

    st.markdown('<p style="color:orange; font-weight:bold; font-size:35px;">Global analysis of recipes</p>', unsafe_allow_html=True)
    st.write("This page presents you a set of analysis on published recipes.")

    st.image(img_1_path)

    # Section 1 : Ingrédients par saisons
    genre = st.radio(
    "Which period do you want ? ",
    ["winter", "spring", "summer","autumn"], index=None,)

    st.write("You selected :", genre)


