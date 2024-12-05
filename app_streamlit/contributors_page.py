import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import seaborn as sns
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from analyse.utils import count_contributors_by_recipe_range_with_bins
from analyse.utils import get_top_tags
from analyse.utils import get_top_ingredients2
from analyse.utils import top_commented_recipes
from analyse.utils import metrics_main_contributor
from analyse.utils import top_contributors_by_recipes

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


def display_contributors_page():
    df_agg = st.session_state.clean_df
    
    st.sidebar.markdown('<h1 style="color:orange;" font-size:24px;">Pick the granularity</h1>', unsafe_allow_html=True)
    
    selected_option = st.sidebar.radio(
        "Select Analysis",
        ("Global contributor's overview", "Focus on a specific contributor"),
        key="analysis_option"
    )

    if selected_option == "Global contributor's overview":
        st.markdown('<p style="color:orange; font-weight:bold; font-size:35px;">Global contributor\'s overview</p>', unsafe_allow_html=True)
        st.write("There is an overview to better understand what makes a good contributor, to make you a better contributor.")

        # Section 1:main metrics
        num_contributors, num_recipes = metrics_main_contributor(df_agg)
        orange1 = (255, 240, 186)
        orange2 = (255, 204, 153)
        icon_contributors = "fas fa-users"
        icon_recipes = "fas fa-utensils"

        col1, col2 = st.columns(2)
        with col1:
            my_metric("Number of Contributors", num_contributors, orange1, icon_contributors)
        with col2:
            my_metric("Number of Recipes", num_recipes, orange2, icon_recipes)

       # Section 1: pie chart
        st.subheader("Distribution of contributors by number of recipes")
        recipe_bins = count_contributors_by_recipe_range_with_bins(df_agg)

        cmap = cm.get_cmap("Oranges", len(recipe_bins))  # Palette "Oranges"
        colors = [cmap(i) for i in range(len(recipe_bins))]

        def round_autopct(pct):
            return '{:.0f}%'.format(pct) if pct > 0 else ''

        # donuts creation
        fig, ax = plt.subplots(figsize=(2, 2))
        ax.pie(
            recipe_bins.values,
            labels=recipe_bins.index,
            autopct=round_autopct,
            startangle=90,
            colors=colors,
            textprops={'fontsize': 5},
            labeldistance=1.1,
            wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
        )

        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig.gca().add_artist(centre_circle)
        st.pyplot(fig)

        # Section 2: Top Contributors
        top_n = st.selectbox("Select the number of top recipes to display:", [3, 5, 10, 15])
        st.subheader(f"Best {top_n} Commented Recipes")
        top_recipes = top_commented_recipes(df_agg, top_n=top_n)

        # graphic
        fig, ax = plt.subplots(figsize=(8, 5))
        y_positions = range(len(top_recipes))
        bars = ax.barh(
            y_positions, 
            top_recipes['num_comments'], 
            color='#FFA500',
            height=0.8
        )

        # labels
        for bar, contributor, recipe in zip(bars, top_recipes['contributor_id'], top_recipes['recipe_id']):
            width = bar.get_width()
            ax.text(
                width + 2, 
                bar.get_y() + bar.get_height() / 2,  
                f'ID: {contributor}',
                va='center',
                fontsize=9
            )

        #  `recipe_id`
        ax.set_yticks(y_positions)
        ax.set_yticklabels(top_recipes['recipe_id'], fontsize=10)
        ax.set_xlabel("Number of Comments", fontsize=12)
        ax.invert_yaxis()  # Inverser pour que le top 1 soit en haut
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        st.pyplot(fig)


        # Section 3: Top Tags
        st.subheader("What are the best tags ?")
        most_commented = st.checkbox("Only most commented recipes", value=False, key="most_commented_checkbox")
        top_n_recipes = st.number_input("How many recipes do you want to analyze:", min_value=1, value=20, step=1, key="num_recipes")
        top_n_tags = st.slider("How many tags you want to display", min_value=5, max_value=50, value=20, key="slider_top_n_tags")
        tags = get_top_tags(df_agg, most_commented=most_commented, top_recipes=top_n_recipes, top_n=top_n_tags)
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
        top_ingredients = get_top_ingredients2(df_agg, df_ingr_map, excluded_ingredients, top_n_ingredients)

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
        
        #section 1 
        st.subheader("Distribution des recettes par contributeur")
        recipe_bins = top_contributors_by_recipes(df_agg, top_n=10)
        st.bar_chart(recipe_bins)


    else:
        st.info("Sélectionnez une analyse à afficher dans la barre latérale.")