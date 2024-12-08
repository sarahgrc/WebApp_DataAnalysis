import streamlit as st
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from load_data.LoadData import DataFrameLoadder
from analyse.utils import unique_ingr, cat_minutes, get_insight_low_ranking, best_recipe_filter_time, visualise_recipe_season, visualise_low_rank_insight
from wordcloud import WordCloud
import random
from analyse.utils import top_recipes
import numpy as np
import plotly.express as px
from analyse.utils import top_recipes_user

#df_ingr_map=pd.read_pickle('../data_files/ingr_map.pkl')




def display_recipes_page(clean_df, df_ingr_map): 
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
        # Nutriment
        option = st.radio(
            "Select a nutrient to display its distribution:",
            ('Calories', 'Total Fat', 'Sugar', 'Sodium', 'Protein', 'Saturated Fat', 'Carbohydrates')
        )
        
        bins = st.slider("Select the number of bins:", min_value=10, max_value=50, value=20, step=5)

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
    # Historgam with KDE courb
    sns.histplot(clean_df[option], bins=bins, kde=True, color=color_map[option])
    plt.xlabel(option, fontsize=14, color='white')
    plt.ylabel('Frequency', fontsize=14, color='white')
    plt.gca().set_facecolor('#0F1116')
    sns.despine()
    st.pyplot(plt)



    # Section : Nutri score
    nutri_score_mapping = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5}
    clean_df["nutri_score_numeric"] = clean_df["nutri_score"].map(nutri_score_mapping)

    nutri_score_colors = {
    "A": "lightgreen", 
    "B": "palegreen", 
    "C": "orange",    
    "D": "lightsalmon",
    "E": "lightcoral"  
    }
    fig = px.scatter(
    clean_df,
    x="nutri_score_numeric", 
    y="num_comments",   
    size="avg_ratings",     
    color="nutri_score",    
    color_discrete_map=nutri_score_colors,  
    title="Relation entre Nutri-Score et Nombre de Commentaires",
    labels={"nutri_score_numeric": "Nutri-Score", "num_comments": "Nombre de Commentaires"},
    )
    st.plotly_chart(fig, use_container_width=True)


    
    st.markdown('<p style="color:orange; font-weight:bold; font-size:35px;">Get some insights </p>', unsafe_allow_html=True)
    
    st.write("\U0001F3AF In this section you will get to see wheter or not some parameter such as the time needed for the recipes could influence your ranking \U0001F3AF")
    
    st.write("Let's start with the season to publish. Is this something you should worry about ?")
    
    st.write("Recipe Visualization by Season (High vs Low Rankings) \U0001F3C6")
    # FIXME add a try catch module --> logg
    fig = visualise_recipe_season(clean_df)
    st.pyplot(fig)    
    df_low_count, df_high_count = get_insight_low_ranking(clean_df)
    fig = visualise_low_rank_insight(df_low_count, df_high_count)
    st.pyplot(fig)
    
    st.markdown("<p style='color:orange; font-weight:bold; font-size:35px;'>Let's get inspired ! </p>", unsafe_allow_html=True)
    st.write("In this section you will get to see 5 stars and more commented recipes filtered on the time needed to prepare them.")
    
    
    opt_time = st.selectbox(
    "Wich time of preparation you want to focus on?",
    ("15 minutes or less", "Between 15 to 30 minutes", "Between 30 minutes to 1 hour", "Between 1 hour to 2 hours", "Between 2 hours to 3 hours", "Between 3 hours to 4 hours", "More than 4 hours"))
    
    # matching user input to functions inputs
    dico_time = {"15 minutes or less" : 'less_15min',
                 "Between 15 to 30 minutes" : '15_30min' ,
                 "Between 30 minutes to 1 hour" :'30min_1h' , 
                 "Between 1 hour to 2 hours" : '1h_2h',
                 "Between 2 hours to 3 hours": '2h_3h',
                 "Between 3 hours to 4 hours" : '3h_4h' ,
                 "More than 4 hours" : '4h_more' }
    
    opt_nb_ex = st.selectbox(
    "How many recipes you want to see ?",
    (1,2,5,10))
    
    exemples_recipes = best_recipe_filter_time(clean_df, dico_time[opt_time], opt_nb_ex)
    if len(exemples_recipes) == 0 : 
        st.write('It seems that no 5 star recipe was found that satisfy this criteria ... Try to visualise fewer exemples or perhaps it is time for you to create the next revolutionnary recipe ! ')
    else : 
        st.write(exemples_recipes)

        
