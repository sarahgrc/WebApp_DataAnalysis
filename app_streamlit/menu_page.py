import streamlit as st
from PIL import Image 
import os

def display_menu_page():
    """
    Display the menu page content.
    """

    st.title("Recipe and User Data Analysis")

    # Display the presentation text
    st.header("Welcome to our web application !")
    st.text("The purpose of this web application is to provide you with the tools to better \n" +
            "understand the data behind recipes and their consumers. Here, you will discover how \n" +
             "users interact with recipe posts on the platform, how recipes are generally \n" 
             "received, and the current trends. But most importantly, you'll learn how you, \n" + 
             "as a prominent contributor, can boost your profile and attract more people \n" +
             "to your publications!")
    st.text("To explore the web app, go to the navigation bar to your left.")
