import pandas as pd
import numpy as np
from os.path import dirname
from os.path import join

__author__ = 'travis-gray'

class ReadInData(object):
    def __init__(self, properties_file, train_file):

        # Data type definition
        self.dtype_dict = {
            'parcelid':                        np.int32,
            'airconditioningtypeid':           np.float64,
            'architecturalstyletypeid':        np.float64,
            'basementsqft':                    np.float64,
            'bathroomcnt':                     np.float64,
            'bedroomcnt':                      np.float64,
            'buildingclasstypeid':             np.float64,
            'buildingqualitytypeid':           np.float64,
            'calculatedbathnbr':               np.float64,
            'decktypeid':                      np.float64,
            'finishedfloor1squarefeet':        np.float64,
            'calculatedfinishedsquarefeet':    np.float64,
            'finishedsquarefeet12':            np.float64,
            'finishedsquarefeet13':            np.float64,
            'finishedsquarefeet15':            np.float64,
            'finishedsquarefeet50':            np.float64,
            'finishedsquarefeet6':             np.float64,
            'fips':                            np.float64,
            'fireplacecnt':                    np.float64,
            'fullbathcnt':                     np.float64,
            'garagecarcnt':                    np.float64,
            'garagetotalsqft':                 np.float64,
            'hashottuborspa':                  np.bool_,
            'heatingorsystemtypeid':           np.float64,
            'latitude':                        np.float64,
            'longitude':                       np.float64,
            'lotsizesquarefeet':               np.float64,
            'poolcnt':                         np.float64,
            'poolsizesum':                     np.float64,
            'pooltypeid10':                    np.float64,
            'pooltypeid2':                     np.float64,
            'pooltypeid7':                     np.float64,
            'propertycountylandusecode':       'str',
            'propertylandusetypeid':           np.float64,
            'propertyzoningdesc':              'str',
            'rawcensustractandblock':          np.float64,
            'regionidcity':                    np.float64,
            'regionidcounty':                  np.float64,
            'regionidneighborhood':            np.float64,
            'regionidzip':                     np.float64,
            'roomcnt':                         np.float64,
            'storytypeid':                     np.float64,
            'threequarterbathnbr':             np.float64,
            'typeconstructiontypeid':          np.float64,
            'unitcnt':                         np.float64,
            'yardbuildingsqft17':              np.float64,
            'yardbuildingsqft26':              np.float64,
            'yearbuilt':                       np.float64,
            'numberofstories':                 np.float64,
            'fireplaceflag':                   np.bool_,
            'structuretaxvaluedollarcnt':      np.float64,
            'taxvaluedollarcnt':               np.float64,
            'assessmentyear':                  np.float64,
            'landtaxvaluedollarcnt':           np.float64,
            'taxamount':                       np.float64,
            'taxdelinquencyflag':              'str',
            'taxdelinquencyyear':              np.float64,
            'censustractandblock':             np.float64,
        }

        # Categorical columns with many unique values
        self.mean_cols = ['propertyzoningdesc',
             'propertycountylandusecode',
             'rawcensustractandblock',
             'regionidcity',
             'regionidneighborhood',
             'regionidzip',
             'censustractandblock',
             'assessmentyear'
            ]

        for column in self.mean_cols:
            self.dtype_dict[column] = 'category'

        # File names
        self.properties_file = properties_file
        self.train_file = train_file

    def import_data(self):
        module_path = dirname(__file__)
        self.train_driver = pd.read_csv(join(module_path, 'data', self.train_file),
                                        parse_dates = ["transactiondate"])

        self.properties = pd.read_csv(join(module_path, 'data', self.properties_file),
                                      dtype=self.dtype_dict)
