import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from analyse.utils import top_recipes

def display_recipes_page(clean_df): 
    """
    Display the recipes page content.
    """
    st.title("Recipes") 

    clean_df = st.session_state.clean_df 

    st.header("Most popular recipes")
    

    """  # Top 5 commented recipes
    top_recipe = st.session_state.clean_df['name'].value_counts().head(5)
    # Convert Series to DataFrame
    top_recipe_df = top_recipe.reset_index() 
    top_recipe_df.columns = ['Recipe', 'Number of comments']
    # Rating mean for each recipe 
    mean_rating_df = (
        st.session_state.clean_df.groupby('name')['rating']
        .mean()
        .reset_index()
        .rename(columns={'rating': 'Mean Rating'})
    )
    # Add the rating mean to the table 
    top_recipe_df = top_recipe_df.merge(mean_rating_df, left_on='Recipe', right_on='name', how='left')
    # remove col 'name' cause redondance
    top_recipe_df.drop(columns=['name'], inplace=True) """

    top_recipe_df = top_recipes(st.session_state.clean_df)
    #Display
    st.table(top_recipe_df)


    my_expander = st.expander(label='Nutritient Distribution options : ')
    with my_expander:
            # Create a radio button to choose the nutrient to plot the distribution
            option = st.radio(
                "Select a nutrient to display its distribution:",
                ('Calories', 'Total Fat', 'Sugar', 'Sodium', 'Protein', 'Saturated Fat', 'Carbohydrates')
    )
    
    plt.figure(figsize=(10, 5))
    sns.histplot(st.session_state.clean_df[option], bins=20, kde=True, color='green')
    plt.xlabel(option)
    plt.ylabel('Frequency')
    st.pyplot(plt)
        

        
