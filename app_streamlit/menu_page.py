import streamlit as st
from PIL import Image 
import os

def display_menu_page():
    """
    Display the menu page content.
    """

        # Get path of the images 
    current_dir = os.path.dirname(__file__)
    images_path = os.path.abspath(os.path.join(current_dir, "..", "images"))
    image_1_path =os.path.join(images_path, "Recette_1.png")
    image_2_path =os.path.join(images_path, "Recette_2.png")   
    
    # Display images
    col1,col2 =st.columns(2, gap = 'small')
    with col1:
        st.image(image_1_path,width=300,use_container_width='never')
    with col2:
        st.image(image_2_path,width=300,use_container_width='never') 


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
