"""
This file will import up to 1M rows from each dataset to facilitate EDA.
"""

import pandas as pd
import numpy as np
import sklearn

os.chdir('/Users/cmarr/Documents/Travis_data_science/Kaggle/zillow')

def property_import():
    return pd.read_csv('/Users/cmarr/Documents/Travis_data_science/Kaggle/zillow/data/properties_2016.csv', index_col='parcelid')

def train_import():
    return pd.read_csv('/Users/cmarr/Documents/Travis_data_science/Kaggle/zillow/data/train_2016.csv', parse_dates = ["transactiondate"], index_col='parcelid')

def clean_properties(prop_df):





if __name__ == '__main__':

    os.chdir('/Users/cmarr/Documents/Travis_data_science/Kaggle/zillow')


    #Import training data
    temp=open('../data/train.csv', 'r')
    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')
    train=pd.read_csv(temp,
                      parse_dates='Date',
                      date_parser=dateparse,
                      index_col=['Store', 'Date'])
    temp.close()
    print(list(train.columns.values)) #file header
    print(train.tail(10)) #last N rows

    #Import test data
    temp=open('../data/test.csv', 'r')
    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')
    test=pd.read_csv(temp,
                     parse_dates='Date',
                     date_parser=dateparse,
                     index_col=['Id', 'Store', 'Date'])
    temp.close()
    print(list(test.columns.values)) #file header
    print(test.tail(10)) #last N rows
