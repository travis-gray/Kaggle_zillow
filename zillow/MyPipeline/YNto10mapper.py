import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

__author__ = 'travis-gray'

class YNto10mapper(BaseEstimator, TransformerMixin):

    def __init__(self, columnNames=[]):
        self.mapping = {'Y': 1, 'N': 0}
        self.__columnnames = columnNames

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, **transform_params):
        # Apply Y-N to 1-0 mapping to column
        df = pd.DataFrame(X)
        for column in self.__columnnames:
            df[column] = df[column].map(self.mapping)
        return df
