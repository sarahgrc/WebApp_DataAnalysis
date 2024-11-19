from code.preprocess.cleaning_data import *
from code.preprocess.merging import *
from tests.conftest import sample_raw_recipes

def test_date_separated(sample_raw_recipes):
    assert len(sample_raw_recipes.columns)==13
    d=date_separated('submitted',sample_raw_recipes)

    #verify specific columns have been added
    assert ('year' in d.columns) 
    assert ('month' in d.columns)
    assert ('day' in d.columns)

    assert len(d) == 200 #verify no rows were removed
 
    assert len(d.columns)==len(sample_raw_recipes.columns)+3 #verify no columns have been removed

def test_outliers(outliers_sample):
    outlier=outliers(outliers_sample, 'A',treshold_sup=30, treshold_inf=None, get_info=False)
    assert isinstance(outlier, list) #verify the type of the output
    assert len(outlier)==6 #verify only values above treshhold are listed

    outlier1=outliers(outliers_sample, 'A',treshold_sup=None, treshold_inf=10, get_info=False)
    assert isinstance(outlier1, list)
    assert len(outlier1)==4

    outlier2=outliers(outliers_sample, 'A',treshold_sup=16, treshold_inf=37, get_info=True)
    assert isinstance(outlier2, pd.DataFrame)
    assert len(outlier2)==7

def test_df_merged(merged_sample):
    df=[merged_sample[0],merged_sample[1]]

    #verify that each type of join return the correct size of dataframe
    type_join=["left", "right", "outer", "inner"]
    for i in type_join:
        merging=dataframe_concat(df,'A',join=i)
        assert len(merging.columns)==3



