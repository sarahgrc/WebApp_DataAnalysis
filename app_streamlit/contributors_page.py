"""This page is dedicated to the page contributor on streamlit, all graphs rely on the contributors' performances
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os

from wordcloud import WordCloud


from analyse.utils import (
    count_contributors_by_recipe_range_with_bins,
    get_top_tags,
    get_top_ingredients2,
    metrics_main_contributor,
    average_and_total_comments_per_contributor,
)

#df_ingr_map = pd.read_pickle("../data_files/ingr_map.pkl")


# Source fonction my_metric : https://py.cafe/maartenbreddels/streamlit-custom-metrics
def my_metric(label, value, bg_color, icon="fas fa-asterisk"):
    fontsize = 18
    lnk = (
        '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" '
        'crossorigin="anonymous">'
    )
    bg_color_css = f'rgb({bg_color[0]}, {bg_color[1]}, {bg_color[2]}, 0.75)'

    htmlstr = f"""
    <p style='background-color: {bg_color_css};
               font-size: {fontsize}px;
               border-radius: 7px;
               padding-left: 12px;
               padding-top: 18px;
               padding-bottom: 18px;
               line-height:25px;'>
               <i class='{icon} fa-xs'></i> {value}
               </style><BR><b><span style='font-size: 15px;
               margin-top: 0;'>{label}</b></style></span></p>
    """

    st.markdown(lnk + htmlstr, unsafe_allow_html=True)


def display_contributors_page(df, df_ingr_map):
    st.sidebar.markdown(
        '<h1 style="color:orange;" font-size:24px;">Analysis Menu</h1>',
        unsafe_allow_html=True,
    )

    current_dir = os.path.dirname(__file__)
    images_path = os.path.abspath(os.path.join(current_dir, "..", "images"))
    img_1_path =os.path.join(images_path, "raw-ingredient.png")

    st.markdown('<p style="color:orange; font-weight:bold; font-size:35px;">Global analysis of recipes</p>', unsafe_allow_html=True)
    st.write("Here, you will find analyses that will allow you to see who the contributors "
             "with the most commented recipes are and what their specificities are (tags, ingredients).")

    st.image(img_1_path)

    selected_page = st.sidebar.radio(
        "Select a page:",
        ("Overview", "Focus Contributor"),
        format_func=lambda x: f"\U0001F50D {x}" if x == "Focus Contributor" else f"\U0001F4CA {x}",
        key="selected_page",
    )

    #section 1 : Graph for overview page
    if selected_page == "Overview":
        st.markdown(
            '<h1 style="color:orange; font-weight:bold; font-size:32px;">General Overview</h1>',
            unsafe_allow_html=True,
        )

        #section 1.1 : main metrics
        num_contributors, num_recipes = metrics_main_contributor(df)
        col1, col2 = st.columns(2)
        with col1:
            my_metric("Number of Contributors", num_contributors, (255, 240, 186), "fas fa-users")
        with col2:
            my_metric("Number of Recipes", num_recipes, (255, 204, 153), "fas fa-utensils")

        st.markdown(
            '<h3 style="color:black; font-size:20px; font-weight:normal;">'
            'Contributors by Recipe Range (Pie Chart)</h3>',
            unsafe_allow_html=True,
        )

        #section 1.2: pie chart contributeurs & number of recipes
        recipe_bins = count_contributors_by_recipe_range_with_bins(df)
        df_plot = recipe_bins.reset_index()
        df_plot.columns = ["Recipe Range", "Contributors"]

        fig_pie = px.pie(
            df_plot,
            names="Recipe Range",
            values="Contributors",
            color="Recipe Range",
            color_discrete_sequence=px.colors.sequential.Oranges,
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_pie, use_container_width=True)

    #section 2 : Focus contributor
    elif selected_page == "Focus Contributor":
        st.markdown(
            '<h1 style="color:orange; font-weight:bold; font-size:32px;">Focus Contributor Analysis</h1>',
            unsafe_allow_html=True,
        )

        filter_option = st.radio(
            "Filter by:",
            ("All Contributors", "Top Contributors", "Most Viewed Recipes"),
            key="filter_option",
        )
        #section 2.1 : filter to display what granularity we want
        if filter_option == "Top Contributors":
            top_n = st.slider("Select number of top contributors:", 1, 10, 5)
            avg_comments_df = average_and_total_comments_per_contributor(df)
            top_contributors = avg_comments_df.nlargest(top_n, "avg_comments_per_recipe")
            filtered_df = df[df["contributor_id"].isin(top_contributors["contributor_id"])]
        elif filter_option == "Most Viewed Recipes":
            filtered_df = df.sort_values(by="num_comments", ascending=False).head(100)
        else:
            filtered_df = df

        st.markdown(
            '<h2 style="color:black; font-size:22px; font-weight:normal;">Top Tags</h2>',
            unsafe_allow_html=True,
        )
        #section 2.2 : Top tag used
        top_n_tags = st.slider("Number of tags to display:", min_value=5, max_value=50, value=10)
        tags = get_top_tags(filtered_df, most_commented=False, top_recipes=20, top_n=top_n_tags)

        if tags.empty:
            st.warning("No tags found in the selected data.")
        else:
            wordcloud = WordCloud(
                width=800, height=400, background_color='white', colormap='Oranges'
            ).generate_from_frequencies(tags)
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)

        #section 2.3 : Top ingredients to display 
        st.markdown(
            '<h2 style="color:black; font-size:22px; font-weight:normal;">Top Ingredients</h2>',
            unsafe_allow_html=True,
        )
        default_excluded = [
            'black pepper', 'vegetable oil', 'salt', 'pepper', 'olive oil', 'oil',
            'butter', 'water', 'sugar', 'flour', 'brown sugar', 'salt and pepper',
            'scallion', 'baking powder', 'garlic', 'flmy', 'garlic clove',
            'all-purpose flmy', 'baking soda', 'ice cube',
        ]
        user_excluded = st.text_area(
            "Exclude ingredients (comma-separated):",
            ", ".join(default_excluded),
            height=100,
        )
        
        excluded_ingredients = set(map(str.strip, user_excluded.split(",")))

        top_n_ingredients = st.slider("Number of ingredients to display:", min_value=5, max_value=50, value=10)
        top_ingredients = get_top_ingredients2(filtered_df, df_ingr_map, excluded_ingredients, top_n_ingredients)

        if top_ingredients.empty:
            st.warning("No ingredients found in the selected data.")
        else:
            fig_ingr = px.bar(
                top_ingredients.reset_index(),
                x="count",
                y="mapped_ingredients",
                orientation="h",
                labels={"count": "Occurrences", "mapped_ingredients": "Ingredient"},
                color="count",
                color_continuous_scale="Oranges",
            )
            fig_ingr.update_layout(template="simple_white")
            st.plotly_chart(fig_ingr, use_container_width=True)