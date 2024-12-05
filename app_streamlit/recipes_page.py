import streamlit as st
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from load_data.LoadData import DataFrameLoadder
from analyse.utils import unique_ingr
from wordcloud import WordCloud
import random

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
    
    top_number_ingr = st.text_area("Enter the amount of ingredients to compare (default set to 200) and select again the season:",'200')
    winter,summer,spring,autumn=unique_ingr(df_agg,df_ingr_map,int(top_number_ingr))

    def word_to_count(lst):
        dico={}
        for i in lst:
            dico[i]=random.randint(10, 100)
        return dico
    
    winter_d=word_to_count(winter)
    sum_d=word_to_count(winter)
    spring_d=word_to_count(spring)
    autumn_d=word_to_count(spring)

    if genre == 'winter :snowflake:':
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(winter_d)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    if genre == 'summer :sunny:':
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(sum_d)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    if genre == 'spring :cherry_blossom:':
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(spring_d)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    if genre == 'autumn :maple_leaf:':
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(autumn_d)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)   


