import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

__author__ = 'travis-gray'

class NanSubs(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.nan_subs = {'airconditioningtypeid': 0, #getdummies
            'architecturalstyletypeid': 0, #getdummies
            'basementsqft': 0,
            'bathroomcnt': 0,
            'bedroomcnt': 0,
            'buildingclasstypeid': 0, #get_dummies
            'buildingqualitytypeid': 0,  #get_dummies
            'calculatedbathnbr': 0,
            'decktypeid': 0, #actually binary
            'finishedfloor1squarefeet': 1348,
            'calculatedfinishedsquarefeet': 1773,
            'finishedsquarefeet12': 1745,
            'finishedsquarefeet13': 1404,
            'finishedsquarefeet15': 2380,
            'finishedsquarefeet50': 1355,
            'finishedsquarefeet6': 2303,
            'fips': 0, #getdummies
            'fireplacecnt': 0,
            'fullbathcnt': 0,
            'garagecarcnt': 0,
            'garagetotalsqft': 0,
            'hashottuborspa': False,
            'heatingorsystemtypeid': 0, #getdummies
            'latitude': 0,
            'longitude': 0,
            # 'lat_bins': 0,
            # 'lon_bins': 0,
            'lotsizesquarefeet': 0, #Lots of heteroscedasticity here, high values have low logerrors
            'poolcnt': 0,
            'poolsizesum': 0, #Could use 520 (mean) here for rows where poolcnt = 1
            'pooltypeid10': 0,
            'pooltypeid2': 0,
            'pooltypeid7': 0,
#             'propertycountylandusecode': '0',
            'propertylandusetypeid': 0,
#             'propertyzoningdesc': '0',
#             'rawcensustractandblock': 0,
#             'regionidcity': 0,
            'regionidcounty': 0, #getdummies
#             'regionidneighborhood': 0,
#             'regionidzip': 0,
            'roomcnt': 0,
            'storytypeid': 0,
            'threequarterbathnbr': 0,
            'typeconstructiontypeid': 0, #getdummies
            'unitcnt': 1,
            'yardbuildingsqft17': 0,
            'yardbuildingsqft26': 0,
            'yearbuilt': 1968,
            'numberofstories': 1,
            'fireplaceflag': False,
            'structuretaxvaluedollarcnt': 180000,  #Lots of heteroscedasticity here, high values have low logerrors
            'taxvaluedollarcnt': 450000,   #Lots of heteroscedasticity here, high values have low logerrors
#             'assessmentyear': 2015,
            'landtaxvaluedollarcnt': 280000, #Lots of heteroscedasticity here, high values have low logerrors
            'taxamount': 6000,   #Lots of heteroscedasticity here, high values have low logerrors
            'taxdelinquencyflag': 'N',
            'taxdelinquencyyear': 16,
#             'censustractandblock': '0'
           }

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        newX = pd.DataFrame(X)
        # Create missing indicators
        for key in self.nan_subs:
            newX[key+'_miss'] = newX[key].isnull()

        # Fill NaN's with imputations
        newX = newX.fillna(self.nan_subs)
        return newX
