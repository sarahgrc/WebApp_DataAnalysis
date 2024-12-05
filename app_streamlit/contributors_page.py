import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from analyse.utils import count_contributors_by_recipe_range_with_bins
from analyse.utils import get_top_tags
from analyse.utils import get_top_ingredients2
from analyse.utils import top_commented_recipes
from analyse.utils import metrics_main_contributor

df_ingr_map = pd.read_pickle("../data_files/ingr_map.pkl")

def my_metric(label, value, bg_color, icon="fas fa-asterisk"):
    fontsize = 18
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    bg_color_css = f'rgb({bg_color[0]}, {bg_color[1]}, {bg_color[2]}, 0.75)'

    htmlstr = f"""<p style='background-color: {bg_color_css}; 
                            font-size: {fontsize}px; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:25px;'>
                            <i class='{icon} fa-xs'></i> {value}
                            </style><BR><b><span style='font-size: 15px; 
                            margin-top: 0;'>{label}</b></style></span></p>"""

    st.markdown(lnk + htmlstr, unsafe_allow_html=True)


def display_contributors_page(df):
    # dfwith recipes in lines 
    st.sidebar.markdown('<h1 style="color:orange;" font-size:24px;">Pick the granularity</h1>', unsafe_allow_html=True)
    
    selected_option = st.sidebar.radio(
        "Select Analysis",
        ("Global contributor's overview", "Focus on a specific contributor"),
        key="analysis_option"
    )

    if selected_option == "Global contributor's overview":
        st.markdown('<p style="color:orange; font-weight:bold; font-size:35px;">Global contributor\'s overview</p>', unsafe_allow_html=True)
        st.write("There is an overview to better understand what makes a good contributor, to make you a better contributor.")

        # Section 0 :main metrics
        num_contributors, num_recipes = metrics_main_contributor(df)
        orange1 = (255, 240, 186)
        orange2 = (255, 204, 153)
        icon_contributors = "fas fa-users"
        icon_recipes = "fas fa-utensils"

        col1, col2 = st.columns(2)
        with col1:
            my_metric("Number of Contributors", num_contributors, orange1, icon_contributors)
        with col2:
            my_metric("Number of Recipes", num_recipes, orange2, icon_recipes)

        # Section 1: Histogram
        # Appel à votre fonction pour obtenir les données
        recipe_bins = count_contributors_by_recipe_range_with_bins(df)

        # Conversion en DataFrame pour Plotly
        df_plot = recipe_bins.reset_index()  # Convertir la série en DataFrame
        df_plot.columns = ["Recipe Range", "Contributors"]  # Renommer les colonnes

        # Création du pie chart avec Plotly
        fig = px.pie(
            df_plot,
            names="Recipe Range",           # Catégories pour le camembert
            values="Contributors",          # Valeurs associées
            color="Recipe Range",           # Coloration par catégorie
            color_discrete_sequence=px.colors.sequential.Oranges,  # Palette de couleurs
        )

        # Personnalisation
        fig.update_traces(
            textposition="inside",          # Position du texte à l'intérieur des sections
            textinfo="percent+label"        # Affiche pourcentage et label
        )
        fig.update_layout(
            showlegend=True,                # Affiche la légende
            template="simple_white"         # Thème clair
        )
        # Affichage dans Streamlit
        st.subheader("Contributors by Recipe Range (Pie Chart)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Section 2: Best Commented Recipes
        st.subheader("Best Commented Recipes")
        top_n = st.selectbox("Select the number of top recipes to display:", [3, 5, 10, 15])
        top_recipes = top_commented_recipes(df, top_n=top_n)  # Cette fonction doit retourner un DataFrame
        st.write("Available columns in DataFrame:", df.columns)
        st.write(df.head())  # Affiche les premières lignes pour inspection

        fig = px.bar(
            top_recipes,
            x="num_comments",              # Nombre de commentaires (axe X)
            y="name",                      # Nom des recettes (axe Y)
            orientation="h",               # Barres horizontales
            text="contributor_id",         # Texte pour identifier les contributeurs
            labels={"num_comments": "Number of Comments", "name": "Recipe Name"},
            color="num_comments",          # Coloration en fonction du nombre de commentaires
            color_continuous_scale="Oranges"  # Palette de couleurs
        )

        # Personnalisation
        fig.update_layout(
            yaxis=dict(
                categoryorder="total ascending"  # Ordre décroissant pour les barres
            ),

            template="simple_white",            # Thème clair et épuré
            height=400 + top_n * 20             # Ajustement dynamique de la hauteur
        )
        # Affichage du graphique dans Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # Section 3: Top Tags
        st.subheader("What are the best tags ?")
        most_commented = st.checkbox("Only most commented recipes", value=False, key="most_commented_checkbox")
        top_n_recipes = st.number_input("How many recipes do you want to analyze:", min_value=1, value=20, step=1, key="num_recipes")
        top_n_tags = st.slider("How many tags you want to display", min_value=5, max_value=50, value=20, key="slider_top_n_tags")
        tags = get_top_tags(df, most_commented=most_commented, top_recipes=top_n_recipes, top_n=top_n_tags)
        wordcloud_input = {tag: count for tag, count in tags.items()}
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(wordcloud_input)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

        # Section 4: Top Ingredients
        st.subheader("Top Ingredients")
        
        default_excluded = ['black pepper', 'vegetable oil', 'salt', 'pepper', 'olive oil', 'oil',
                            'butter', 'water', 'sugar', 'flour', 'brown sugar', 'salt and pepper',
                            'scallion', 'baking powder', 'garlic', 'flmy', 'garlic clove',
                            'all-purpose flmy', 'baking soda']
        user_excluded = st.text_area("Enter ingredients to exclude, separated by commas:", ", ".join(default_excluded))
        excluded_ingredients = set(map(str.strip, user_excluded.split(",")))
        top_n_ingredients = st.number_input("Select the number of top ingredients to display:", min_value=1, value=10, step=1, key="number_top_ingredients")
        top_ingredients = get_top_ingredients2(df, df_ingr_map, excluded_ingredients, top_n_ingredients)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=top_ingredients.reset_index(), x='mapped_ingredients', y='count', ax=ax, color='orange')
        ax.set_ylabel('Number of occurencies')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        st.pyplot(fig)


    elif selected_option == "Focus on a specific contributor":
        st.markdown('<p style="color:orange; font-weight:bold; font-size:35px;">Focus on a specific contributor</p>', unsafe_allow_html=True)
        # Aadd 


    else:
        st.info("Sélectionnez une analyse à afficher dans la barre latérale.")