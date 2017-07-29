from .ImportData import ReadInData
import pandas as pd
import numpy as np

__author__ = 'travis-gray'


class CreateDatasets(ReadInData):
    '''
    Creating training X and Y and scoring X datasets

    Appending means of categorical variables is done in this step since
    it requires the full X inclusive of properties not sold and sklearn does
    not support that functionality within pipelines (as far as I can tell)
    '''
    def __init__(self, **kwargs):
        super(CreateDatasets, self).__init__(**kwargs)

        # Create a container for X datasets
        self.Xs = {'x_train': pd.DataFrame(), 'x_scoring': pd.DataFrame()}

        # Special columns to treat differently
        self.drop_indices = ['parcelid']
        self.y_col = 'logerror'

        self.mean_col_dfs_ = {}

    def calculate_categorical_mean_logerror(self, df, cat_column):
        categorical_means = (df[['logerror', cat_column]]
                                          .groupby(cat_column)
                                          .agg({'logerror': 'mean'})
                                          .rename(columns={'logerror': cat_column+'_mean'}))
        categorical_means.reset_index(inplace=True)
        categorical_means[cat_column+'_mean'].fillna(0, inplace=True)
        return categorical_means

    def create_scoring_driver(self, properties_df):
        # Start by identifying unique parcels
        parcels = properties_df.parcelid.unique()

        # Adding to a dataframe with a dummy variable that will allow a cross join in the next step
        parcels_df = pd.DataFrame({'parcelid': parcels, 'dummy': np.zeros(len(parcels))})

        #Create a row for each parcel for each month to be scored
        trxn_months = pd.DataFrame({'transactiondate': ['2016/10/01', '2016/11/01', '2016/12/01', '2017/10/01', '2017/11/01', '2017/12/01'],
                            'dummy': np.zeros(6)})
        trxn_months.transactiondate = pd.to_datetime(trxn_months.transactiondate)

        # Finally create the driver for scoring
        return pd.merge(parcels_df, trxn_months, how='outer', on='dummy').drop('dummy', axis=1)

    def run(self):
        self.import_data()

        train = pd.merge(self.properties, self.train_driver, how='left', on='parcelid')
        # Null values of latitude indicate properties that don't need to be in the training dataset
        # They still need to be included in the scoring dataset
        train = train[train.latitude.notnull()]
        self.y_train = train[self.y_col]
        self.Xs['x_train'] = train.drop(self.drop_indices+[self.y_col], axis=1)

        self.scoring_driver = self.create_scoring_driver(self.properties)
        self.scoring = pd.merge(self.scoring_driver, self.properties, how='left', on='parcelid')
        self.Xs['x_scoring'] = self.scoring.drop(self.drop_indices, axis=1)



        # Calculate categorical means
        for column in self.mean_cols:
            self.mean_col_dfs_[column] = self.calculate_categorical_mean_logerror(df=train, cat_column=column)

        self.Xs['x_train'] = self.Xs['x_train'][self.Xs['x_train']['transactiondate'].notnull()]
        self.y_train = self.y_train[self.y_train.notnull()]

        # Perform transforms that won't work in the pipeline:
        # - Drop transactiondate
        # - Append categorical means to training and scoring x files
        for key, dataset in self.Xs.items():
            # Transaction month
            self.Xs[key]['transaction_month'] = self.Xs[key]['transactiondate'].dt.month
            self.Xs[key].drop('transactiondate', axis=1, inplace=True)
            for column in self.mean_cols:
                self.Xs[key] = pd.merge(self.Xs[key], self.mean_col_dfs_[column], how='left', on=column)
                self.Xs[key].drop(column, axis=1, inplace=True)
                self.Xs[key][column+'_mean_miss'] = self.Xs[key][column+'_mean'].isnull()
                self.Xs[key][column+'_mean'].fillna(0, inplace=True)
