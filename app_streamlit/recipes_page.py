import streamlit as st
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from load_data.LoadData import DataFrameLoadder
from analyse.utils import unique_ingr
from wordcloud import WordCloud

df_ingr_map=pd.read_pickle('../data_files/ingr_map.pkl')

def display_recipes_page():
    """
    Display the recipes page content.
    """
    df_agg = st.session_state.clean_df
    
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
    ["winter :snowflake:", "spring :cherry_blossom:", "summer :sunny:","autumn :maple_leaf:"], index=None,)

    st.write("You selected :", genre)
    
    top_number_ingr = st.text_area("Enter the amount of ingredients to compare (default set to 200):",)
    unique_ingredients=unique_ingr(df_agg,df_ingr_map,top_number_ingr)

    wordcloud_input = {tag: count for tag, count in unique_ingredients.items()}
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(wordcloud_input)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)