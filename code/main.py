from preprocess.clean_dataframe import *

#create the clean dataframe 
clean_df=prepare_final_dataframe(pd.read_csv('data_files/RAW_interactions.csv'),pd.read_csv('data_files/RAW_recipes.csv'),pd.read_csv('data_files/PP_recipes.csv'))


