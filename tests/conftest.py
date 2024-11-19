import pandas as pd
import numpy as np
import pytest

@pytest.fixture
def sample_raw_recipes():
    df=pd.read_csv('sample/sample_raw_recipes.csv')
    return df

@pytest.fixture
def outliers_sample():
    df=pd.DataFrame({'A': np.arange(0,50,3),'B':np.arange(20,70,3)})
    return df

@pytest.fixture
def merged_sample():
    df1=pd.DataFrame({'A': np.arange(0,50,3),'B':np.arange(20,70,3)})
    df2=pd.DataFrame({'A': np.arange(0,50,3),'C':np.arange(100,150,3)})
    return df1,df2