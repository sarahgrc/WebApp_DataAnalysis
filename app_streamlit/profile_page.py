import streamlit as st 
import pandas as pd 
from .analyse.utils import user_recipes
from .analyse.utils import top_recipes_user
from .analyse.utils import top_recipes

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

def display_profile_page(clean_df, user_id = 47892):
    """
    Display the profile page content.
    
    Args:
        clean_df (pd.DataFrame): DataFrame containing recipe data.
        user_id (int, optional): The ID of the user. Default is 47892.

    Returns:
        None
    """ 

    clean_df = st.session_state.clean_df 
    st.title("Profile Analysis")
    st.write("Here you will find some metrics about your profile.")
    
    # Dropdown to choose user   
    user_id = st.selectbox("Select User", clean_df['contributor_id'].unique())

    if user_id:
        # Add button to allow user to choose to analyze the profile
        if st.button("Analyze Profile"):
            title = "Profile tracking : User " + str(user_id) 
            st.markdown('<p style="color:orange; font-weight:bold; font-size:35px;">' +  "Profile tracking : User " + str(user_id) +'</p>', unsafe_allow_html=True)

            # Filter data for the given user
            user_recipes_df = user_recipes(clean_df, user_id)

            # Check if user has data
            if user_recipes_df.empty:
                st.warning("No data available for this user.")
                return 

            # Get top recipes using the existing function
            top_recipes_df = top_recipes_user(user_recipes_df)

            # Calculate metrics
            nb_com_mean = user_recipes_df['num_comments'].mean()
            rating_mean = user_recipes_df['avg_reviews'].mean()

            # Display metrics
            rose = (240, 135, 114)
            coral = (200, 90, 80)
            icon_com = "fas fa-solid fa-comment"
            icon_rating = "fas fa-solid fa-star"

            col1, col2 = st.columns(2)
            with col1:
                my_metric("Average comments by recipe", round(nb_com_mean, 2), rose, icon_com)
            with col2:
                my_metric("Average rating", round(rating_mean, 2), coral, icon_rating)

            # Display top recipes
            st.markdown('<p style="color:orange; font-weight:bold; font-size:35px;">' +  "Your 5 most popular recipes :" + '</p>', unsafe_allow_html=True)
            st.table(top_recipes_df)
    else:
        st.write("Please select a user to analyze.")
