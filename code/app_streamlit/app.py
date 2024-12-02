import streamlit as st
from menu_page import display_menu_page 
from contributors_page import display_contributors_page
from recipes_page import display_recipes_page 
from profile_page import display_profile_page
# Set the page configuration
st.set_page_config(page_title="Data Manager", page_icon=":material/edit:")

# Initialize session state for login status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False 

# Define the main function
def main(): 
    """
    Display the main  page of the web app
    """

    # Show login message if not logged in
    if not st.session_state.logged_in:
        st.title("Recipe and Consumer Analysis")
        st.write("Welcome to the web app : Recipe and consumer analysis!")
        st.write("Please log in to the application.")
        if st.button("Log in"):
            st.session_state.logged_in = True  # Set login state
    else:
        # Show account and report pages if logged in
        menu_page = st.Page(display_menu_page, title="Menu", icon=":material/thumb_up:")
        contributors_page = st.Page(display_contributors_page, title="Contributors", icon=":material/dashboard:")
        recipes_page = st.Page(display_recipes_page, title="Recipe", icon=":material/dashboard:")
        profile_page = st.Page(display_profile_page, title="Profile", icon=":material/dashboard:")
        pg = st.navigation([menu_page, contributors_page, recipes_page, profile_page])

        # Run the navigation
        pg.run()


if __name__ == "__main__":
    main()
