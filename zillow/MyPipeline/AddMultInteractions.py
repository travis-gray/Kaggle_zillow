import pandas as pd
import numpy as np
import itertools
from sklearn.base import BaseEstimator, TransformerMixin

__author__ = 'travis-gray'

class AddMultInteractions(BaseEstimator, TransformerMixin):

    def __init__(self, columns=[]):
        self.__columns = columns

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, **transform_params):
        if len(self.__columns) > 0:
            itercols = self.__columns
        else:
            itercols = X.columns

        pairs = list(itertools.combinations(itercols, 2))
        for (column1, column2) in pairs:
            X[column1 + '_'+ column2 + '_mult_intx'] = X[column1] * X[column2]
        return X
