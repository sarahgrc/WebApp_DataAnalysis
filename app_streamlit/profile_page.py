import streamlit as st 
import pandas as pd 
from analyse.utils import user_recipes

username = 47892

# Source fonction my_metric : https://py.cafe/maartenbreddels/streamlit-custom-metrics
def my_metric(label, value, bg_color, icon="fas fa-asterisk"):
    fontsize = 18
    valign = "left"      
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

def display_profile_page(clean_df):
    """
    Display the profile  page content.
    """
    st.title("Profile tracking : User " + str(username))

    user_recipes_df = user_recipes(clean_df, username)

    print("USER RECIPES")
    print(user_recipes_df.head())
    print(user_recipes_df.info())

    # Top 5 recettes commentées de l'user 
    top_user_recipe = user_recipes_df['name'].value_counts().head(5) 
    # Convertir la Série en DataFrame 
    top_user_recipe_df = top_user_recipe.reset_index()
    top_user_recipe_df.columns = ['Recipe', 'Number of comments']

    # top_user_recipe.rename(columns={'value': 'Number'}, inplace = True)
    
    # Moyenne com par recette = Nb de com / Nb de recettes 
    nb_com_mean = user_recipes_df['name'].value_counts().mean()  
    rating_mean = user_recipes_df['rating'].mean()

    # Display
    blue = (51, 144, 255)
    red = (204, 0, 102)
    icon_com = "fas fa-solid fa-comment"
    icon_rating = "fas fa-solid fa-star"

    col1, col2 = st.columns(2)
    with col1:
        my_metric("Average comments by recipe", nb_com_mean, blue, icon_com)
    with col2:
        my_metric("Average rating", rating_mean, blue, icon_rating)

    # st.metric(label="Average comments by recipe", value=nb_com_mean, delta=123, delta_color="off")
    # st.metric(label="Average rating", value=rating_mean, delta=123, delta_color="off")
    st.header("Your 5 most popular recipes : ")
    st.table(top_user_recipe_df)
