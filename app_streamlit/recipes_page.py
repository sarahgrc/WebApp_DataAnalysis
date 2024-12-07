import streamlit as st
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from load_data.LoadData import DataFrameLoadder
from analyse.utils import unique_ingr, cat_minutes, get_insight_low_ranking, best_recipe_filter_time, visualise_recipe_season, visualise_low_rank_insight
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


    
    st.markdown('<p style="color:orange; font-weight:bold; font-size:35px;">Get some insights </p>', unsafe_allow_html=True)
    
    st.write("\U0001F3AF In this section you will get to see wheter or not some parameter such as the time needed for the recipes could influence your ranking \U0001F3AF")
    
    st.write("Let's start with the season to publish. Is this something you should worry about ?")
    
    st.write("Recipe Visualization by Season (High vs Low Rankings) \U0001F3C6")
    # FIXME add a try catch module --> logg
    fig = visualise_recipe_season(df_agg)
    st.pyplot(fig)
    
    df_low_count, df_high_count = get_insight_low_ranking(df_agg)
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
    
    exemples_recipes = best_recipe_filter_time(df_agg, dico_time[opt_time], opt_nb_ex)
    if len(exemples_recipes) == 0 : 
        st.write('It seems that no 5 star recipe was found that satisfy this criteria ... Try to visualise fewer exemples or perhaps it is time for you to create the next revolutionnary recipe ! ')
    else : 
        st.write(exemples_recipes)
    
    

