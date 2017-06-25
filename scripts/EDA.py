"""
Exploratory data analysis

"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
color = sns.color_palette()

%matplotlib inline

pd.options.mode.chained_assignment = None
pd.options.display.max_columns = 999

if __name__ == '__main__':

    os.chdir('/Users/cmarr/Documents/Travis_data_science/Kaggle/zillow')

    #Explore store dataset
    print stores.columns.values
    store_columns=stores.columns.values
    for column in store_columns:
        print stores.groupby(column).size()
        print stores[column].isnull().sum()

    stores_copy = stores

    def dateify(row):
        try:
            row['CompetitionOpenSinceYear'].isnull()
        except:
            pass
        else:
            return pd.datetime.strptime(str(int(row['CompetitionOpenSinceYear']))+' '+
                           str(int(row['CompetitionOpenSinceMonth'])),'%Y %m').date()

    stores_copy['Competition_open_dt']=str(stores_copy['CompetitionOpenSinceYear']).strip()\
        +str(stores_copy['CompetitionOpenSinceMonth']).strip()
    stores_copy['Competition_open_dt']=stores_copy.apply(lambda row: dateify(row), axis=1)
    print stores_copy.head()
