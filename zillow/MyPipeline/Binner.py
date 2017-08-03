import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

__author__ = 'travis-gray'

class Binner(BaseEstimator, TransformerMixin):

    def __init__(self, columnname, num_bins):
        self.__columnname = columnname
        self.__num_bins = num_bins

    def fit(self, X, y=None, **fit_params):
        trash1, self.columnname_bins_ = pd.cut(X[self.__columnname],
                                               bins=self.__num_bins,
                                               labels=False, retbins=True)
        return self

    def transform(self, X, **transform_params):
        newX = pd.DataFrame(X)
        newX[self.__columnname + '_bins'] = pd.cut(newX[self.__columnname],
                                                   bins=self.columnname_bins_,
                                                   labels=np.arange(self.__num_bins))
        return newX
