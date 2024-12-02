import streamlit as st 
import pandas as pd 

username = 47892

def display_profile_page():
    """
    Display the profile  page content.
    """
    st.title("Profile tracking : User " + str(username))
