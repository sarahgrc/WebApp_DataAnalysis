import streamlit as st
import pandas as pd
from menu_page import display_menu_page
from contributors_page import display_contributors_page
from recipes_page import display_recipes_page
from profile_page import display_profile_page
from load_data.preprocess.clean_dataframe import prepare_final_dataframe

# Set the page configuration
st.set_page_config(page_title="Data Manager", page_icon=":material/edit:")

# Initialize session state for login status and clean_df
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "clean_df" not in st.session_state:
    # Executed only once per session
    st.session_state.clean_df = prepare_final_dataframe(
        pd.read_csv('../data_files/RAW_interactions.csv'),
        pd.read_csv('../data_files/RAW_recipes.csv'),
        pd.read_csv('../data_files/PP_recipes.csv')
    ).head(1000)

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
        # Sidebar navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.radio(
            "Select a page",
            ["Menu", "Contributors", "Recipes", "Profile"]
        )

        # Page display logic
        if page == "Menu":
            display_menu_page()
        elif page == "Contributors":
            display_contributors_page(clean_df)
        elif page == "Recipes":
            display_recipes_page()
        elif page == "Profile":
            display_profile_page(clean_df)

if __name__ == "__main__":
    main()
