import streamlit as st
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from load_data.LoadData import DataFrameLoadder
from analyse.utils import unique_ingr
from wordcloud import WordCloud
import random
from analyse.utils import top_recipes
import numpy as np
import plotly.express as px
from analyse.utils import top_recipes_user

df_ingr_map=pd.read_pickle('data_files/ingr_map.pkl')




def display_recipes_page(clean_df): 
    """
    Display the recipes page content.
    """
    st.title("Recipes")

    clean_df = st.session_state.clean_df

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
    winter,summer,spring,autumn=unique_ingr(clean_df,df_ingr_map,int(top_number_ingr))

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

    # Section : Most popular recipes

    st.markdown('<p style="color:orange; font-weight:bold; font-size:35px;">Most popular recipes</p>', unsafe_allow_html=True)
    top_recipe_df = top_recipes(clean_df)
    #Display
    st.table(top_recipe_df)
    
    # Section : Distribution nutrients
    st.markdown('<p style="color:orange; font-weight:bold; font-size:35px;">Nutrients analysis</p>', unsafe_allow_html=True)
    
    my_expander = st.expander(label='Nutritient Distribution options :')
    with my_expander:
        # Sélectionner le nutriment à afficher
        option = st.radio(
            "Select a nutrient to display its distribution:",
            ('Calories', 'Total Fat', 'Sugar', 'Sodium', 'Protein', 'Saturated Fat', 'Carbohydrates')
        )
        
        # Créer un slider pour le nombre de bins
        bins = st.slider("Select the number of bins:", min_value=10, max_value=50, value=20, step=5)

    # Palette pour chaque nutriment
    color_map = {
        'Calories': 'orange',
        'Total Fat': 'beige',
        'Sugar': 'pink',
        'Sodium': 'blue',
        'Protein': 'green',
        'Saturated Fat': 'purple',
        'Carbohydrates': 'brown'
    }
    plt.figure(figsize=(10, 5), facecolor='#0F1116')
    # Without grids
    sns.set_theme(style='white')  
    # Historgam with KDE cpurb
    sns.histplot(clean_df[option], bins=bins, kde=True, color=color_map[option])
    plt.xlabel(option, fontsize=14, color='white')
    plt.ylabel('Frequency', fontsize=14, color='white')
    plt.gca().set_facecolor('#0F1116')
    sns.despine()
    st.pyplot(plt)



    # Section : Nutri score

    # Convertir le Nutri-Score en valeurs numériques (si nécessaire)
    nutri_score_mapping = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
    clean_df["nutri_score_numeric"] = clean_df["nutri_score"].map(nutri_score_mapping)

    nutri_score_colors = {
    "A": "lightgreen",  # Vert pastel
    "B": "palegreen",   # Vert clair
    "C": "orange",      # Orange pastel
    "D": "lightsalmon", # Rouge clair
    "E": "lightcoral"   # Rouge pastel
    }
    fig = px.scatter(
    clean_df,
    x="nutri_score_numeric",  # Numérique pour Nutri-Score
    y="num_comments",         # Nombre de commentaires
    size="avg_ratings",       # Taille basée sur la moyenne des évaluations
    color="nutri_score",      # Couleur basée sur le Nutri-Score
    color_discrete_map=nutri_score_colors,  # Appliquer la palette définie
    title="Relation entre Nutri-Score et Nombre de Commentaires",
    labels={"nutri_score_numeric": "Nutri-Score", "num_comments": "Nombre de Commentaires"},
    )

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig, use_container_width=True)
        
