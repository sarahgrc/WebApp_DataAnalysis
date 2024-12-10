import streamlit as st
import pandas as pd
from .menu_page import display_menu_page
from .contributors_page import display_contributors_page
from .recipes_page import display_recipes_page
from .profile_page import display_profile_page
from .load_data import LoadData
from .load_data.LoadData import DataFrameLoadder
import os
import zipfile
import gdown


# Wrapper functions for pages
def display_recipes_page_wrapper():
    display_recipes_page(st.session_state.clean_df, st.session_state.df_ingr_map) 

def display_profile_page_wrapper():
    display_profile_page(st.session_state.clean_df)

def display_contributors_page_wrapper():
    display_contributors_page(st.session_state.clean_df, st.session_state.df_ingr_map)

# Define the main function
def main():
    """
    Display the main page of the web app
    """
    # Load pages for navigation
    menu_page = st.Page(display_menu_page, title="Menu", icon=":material/thumb_up:")
    contributors_page = st.Page(display_contributors_page_wrapper, title="Contributors", icon=":material/dashboard:")
    recipes_page = st.Page(display_recipes_page_wrapper, title="Recipes", icon=":material/dashboard:")
    profile_page = st.Page(display_profile_page_wrapper, title="Your Profile", icon=":material/dashboard:")
    pg = st.navigation([menu_page, contributors_page, recipes_page, profile_page])

    # Run the navigation
    pg.run()

if __name__ == "__main__":
    # Set the page configuration
    st.set_page_config(page_title="Data Manager", page_icon=":material/edit:")

    # Initialize session state for clean_df
    if "clean_df" not in st.session_state:
        # Executed only once per session
        DF = DataFrameLoadder(path_raw_interaction='./data_files/df_preprocess.csv')
        df = DF.load()
        st.session_state.clean_df = df

    if "df_ingr_map" not in st.session_state:
        df_ingr_map = pd.read_pickle("./data_files/ingr_map.pkl")
        st.session_state.df_ingr_map = df_ingr_map

    main()
