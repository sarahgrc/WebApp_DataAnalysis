import streamlit as st
from account import display_account_page 
from page_template import display_report_page  

# Set the page configuration
st.set_page_config(page_title="Data Manager", page_icon=":material/edit:")

# Initialize session state for login status
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False 

# Define the main function
def main():
    st.title("Recipe Analysis")
    st.write("Welcome to my app!")

    # Show login message if not logged in
    if not st.session_state.logged_in:
        st.write("Please log in to access the account and report pages.")
        if st.button("Log in"):
            st.session_state.logged_in = True  # Set login state
    else:
        # Show account and report pages if logged in
        account_page = st.Page(display_account_page, title="Account", icon=":material/thumb_up:")
        report_page = st.Page(display_report_page, title="Report 1", icon=":material/dashboard:")
        pg = st.navigation([account_page, report_page])

        # Run the navigation
        pg.run()

# Run the main function
if __name__ == "__main__":
    main()
