import streamlit as st
import pandas as pd
from menu_page import display_menu_page
from contributors_page import display_contributors_page
from recipes_page import display_recipes_page
from profile_page import display_profile_page
from load_data.LoadData import DataFrameLoadder
import os
import zipfile
import gdown

# download all the necesary files for the project 

zip_url =   'https://drive.google.com/file/d/1D79eoCITGfd9yz0cWDzQsxoL7TwadWC_/view?usp=sharing'  #'https://drive.google.com/file/d/11KFS8Kiyivn0vvaOJwHiNo42CAduzLuV/view?usp=drive_link'
file_id = zip_url.split('/d/')[1].split('/')[0]
download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
folder_storage = '../data_files'


def download_extract_zip(gdrive_url, out_dir):
    """
    Download a google drive Zip archive and extract it to wanted folder

    Args:
        gdrive_url (str): Google Drive url of the download zip archive.
        out_dir (str): Path where to extract the zip files.
    """
    # create output path if not existing
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    try:
        # Download zip file
        local_zip_path = os.path.join(out_dir, "data.zip")
        gdown.download(gdrive_url, local_zip_path, quiet=False)

        # Extract zip file
        with zipfile.ZipFile(local_zip_path, 'r') as zipf:
            zipf.extractall(out_dir)
            print(' -- Extraction terminée --')
        
        # Remove zip file
        os.remove(local_zip_path)
    except Exception as e:
        print("*** ERREUR ***", e)




#wrapper functions for pages
def display_recipes_page_wrapper():
    display_recipes_page(st.session_state.clean_df , st.session_state.df_ingr_map) 

def display_profile_page_wrapper():
    display_profile_page(st.session_state.clean_df)

def display_contributors_page_wrapper():
    display_contributors_page(st.session_state.clean_df, st.session_state.df_ingr_map)

# Define the main function
def main():
    """
    Display the main page of the web app
    
    """

    clean_df = st.session_state.clean_df  # Retrieve the data from session state


    # Show login message if not logged in
    if not st.session_state.logged_in:
        st.title("Recipe and User Data Analysis")
        st.write("Welcome to the web app: Recipe and consumer analysis!")
        st.write("Please log in to the application.")
        if st.button("Log in"):
            st.session_state.logged_in = True  # Set login state
    else:
        # Show account and report pages if logged in
        menu_page = st.Page(display_menu_page, title="Menu", icon=":material/thumb_up:")
        contributors_page = st.Page(display_contributors_page_wrapper, title="Contributors", icon=":material/dashboard:")
        recipes_page = st.Page(display_recipes_page_wrapper,  title="Recipes", icon=":material/dashboard:")
        profile_page = st.Page(display_profile_page_wrapper, title="Your profile", icon=":material/dashboard:")
        pg = st.navigation([menu_page, contributors_page, recipes_page, profile_page])

        # Run the navigation
        pg.run()

if __name__ == "__main__":
    
    if not os.path.exists('../data_files/RAW_interactions.csv') : 
        download_extract_zip(download_url, folder_storage)
    
      
    # Set the page configuration
    st.set_page_config(page_title="Data Manager", page_icon=":material/edit:")

    # Initialize session state for login status and clean_df
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "clean_df" not in st.session_state:
        # cheking existance correct  
        print(f"PP_recipes : {os.path.exists('../data_files/PP_recipes.csv')} , col : {pd.read_csv('../data_files/PP_recipes.csv').columns}")
        print(f"RAW_recipes : {os.path.exists('../data_files/RAW_recipes.csv')} , col = {pd.read_csv('../data_files/RAW_recipes.csv').columns}")
        print(f"RAW_interactions : {os.path.exists('../data_files/RAW_interactions.csv')}, col = {pd.read_csv('../data_files/PP_recipes.csv').columns}")
        
        # Executed only once per session
        DF = DataFrameLoadder(path_raw_interaction='../data_files/RAW_interactions.csv',
                              path_raw_recipes='../data_files/RAW_recipes.csv',
                              pp_recipe='../data_files/PP_recipes.csv')
        df = DF.load()
        st.session_state.clean_df = df
        
    if "df_ingr_map" not in st.session_state:
        df_ingr_map = pd.read_pickle("../data_files/ingr_map.pkl")
        st.session_state.df_ingr_map = df_ingr_map
    main()
