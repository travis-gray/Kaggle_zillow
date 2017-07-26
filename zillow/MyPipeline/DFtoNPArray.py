import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

__author__ = 'travis-gray'

class DFtoNPArray(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, **transform_params):
        return X.as_matrix().astype(np.float)
