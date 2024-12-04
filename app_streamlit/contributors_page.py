import streamlit as st 
import pandas as pd
import seaborn as sns
import ast
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from load_data.preprocess.clean_dataframe import prepare_final_dataframe
from analyse.utils import count_contributors_by_recipe_range_with_bins
from analyse.utils import top_contributors_by_commented_recipes
from analyse.utils import top_tags
from analyse.utils import get_top_ingredients
from analyse.utils import top_contributors_by_recipes
from load_data.LoadData import DataFrameLoadder

clean_df = DataFrameLoadder(path_raw_interaction='../data_files/RAW_interactions.csv',
                      path_raw_recipes='../data_files/RAW_recipes.csv',
                      pp_recipe='../data_files/PP_recipes.csv').load()

df_ingr_map=pd.read_pickle('../data_files/ingr_map.pkl')

def display_contributors_page():
    st.sidebar.markdown('<h1 style="color:orange;"font-size:24px;">Choisis tes analyses</h1>', unsafe_allow_html=True)
    show_global_view = st.sidebar.button("Vue globale des contributeurs")
    focus_contributor = st.sidebar.button("Focus sur un contributeur")

    if show_global_view:
        st.markdown('<p style="color:orange; font-weight:bold; font-size:35px;">Analyse Globale des Contributeurs</p>', unsafe_allow_html=True)
        st.write("Voici une vue d'ensemble des contributeurs et leurs impacts sur les recettes.")
        
        # Section 1: Large Graph (Full Width)
        st.subheader("Distribution des recettes par contributeurs")
        top_n = st.slider("Nombre de contributeurs à afficher", min_value=5, max_value=20, value=10,key='section1slider')
        recipe_bins = count_contributors_by_recipe_range_with_bins(clean_df)
        fig, ax = plt.subplots(figsize=(15, 6))
        sns.barplot(x=recipe_bins.index, y=recipe_bins.values, ax=ax, palette=["orange"])
        for i, value in enumerate(recipe_bins.values):
            ax.text(i, value + 0.5, str(value), ha="center", va="bottom", fontsize=10, color="black")
        ax.yaxis.set_visible(False)
        ax.set_xticklabels(recipe_bins.index, rotation=45)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        st.pyplot(fig)

        # Section 2: Top Commenters (Below Large Graph)
        st.subheader("Les contributeurs ayant les recettes les plus commentées")
        top_n = st.slider("Nombre de contributeurs à afficher", min_value=5, max_value=20, value=10,key='section2slider')
        top_commenters = top_contributors_by_commented_recipes(clean_df, top_n=top_n)
        st.write(top_commenters)

        # Section 3: Top Tags and Ingredients (Side-by-Side)
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Les meilleurs tags utilisés")
            top_n = st.slider("Nombre de tags à afficher", min_value=5, max_value=50, value=20)
            tags = top_tags(clean_df, top_n=top_n)
            wordcloud_input = {tag: count for tag, count in tags.items()}
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(wordcloud_input)
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)

        with col2:
	        # Allow user to exclude specific ingredients
            default_excluded = ['black pepper', 'vegetable oil', 'salt', 'pepper', 'olive oil', 'oil',
	                            'butter', 'water', 'sugar', 'flour', 'brown sugar', 'salt and pepper',
	                            'scallion', 'baking powder', 'garlic', 'flmy', 'garlic clove',
	                            'all-purpose flmy', 'baking soda']
            user_excluded = st.text_area("Enter ingredients to exclude, separated by commas:", ", ".join(default_excluded))
            excluded_ingredients = set(map(str.strip, user_excluded.split(",")))
            top_n = st.number_input("Select the number of top ingredients to display:", min_value=1, value=10, step=1)
            top_ingredients = get_top_ingredients(clean_df, df_ingr_map, excluded_ingredients, top_n)
            st.subheader("Top Ingredients")
            st.write(top_ingredients)
	
	        # Generate and display word cloud
            st.subheader("Ingredient Word Cloud")
            wordcloud_input = {ingredient: count for ingredient, count in top_ingredients.items()}
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(wordcloud_input)
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)
    else:
        st.info("Sélectionnez une analyse à afficher dans la barre latérale.")