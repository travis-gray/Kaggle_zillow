import numpy as np
import pandas as pd

from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import metrics
from os.path import join
import os

from Imports.CreateDatasets import CreateDatasets

from MyPipeline.NanSubs import NanSubs
# from MyPipeline.Binner import Binner
from MyPipeline.YNto10mapper import YNto10mapper
from MyPipeline.DFtoNPArray import DFtoNPArray

def main():
    drivers = CreateDatasets(properties_file='properties_2016.csv',
                             train_file='train_2016_v2.csv')
    drivers.run()

    X_train, X_test, y_train, y_test = train_test_split(drivers.Xs['x_train'], drivers.y_train, random_state=8675309)
    params = {'n_estimators': 800,
              'learning_rate': 0.01,
              'max_depth': 6,
              'min_samples_leaf': 25,
              'subsample': 0.5,
              'max_features': 0.5
              }
    gbm = GradientBoostingRegressor(loss='lad', random_state=90210, **params)

    print('Starting pipeline')
    pipeline = Pipeline(
        [
            ('basefeatures', NanSubs()),
            ('trxndqflag', YNto10mapper(['taxdelinquencyflag'])),
            ('numpyarray', DFtoNPArray()),
            ("gbm", gbm)
        ]
    )

    # cross_val_score(pipeline, drivers.Xs['x_train'], drivers.y_train, cv=5, scoring='mean_absolute_error')
    # pipeline.fit(drivers.Xs['x_train'], drivers.y_train)
    pipeline.fit(X_train, y_train)
    print('Finished pipeline')
    pred = pipeline.predict(X_test)

    # score on test data (accuracy)
    mae = mean_absolute_error(y_test, pred)
    orig_mae = mean_absolute_error(drivers.y_train, np.zeros(len(drivers.y_train)))

    print('MAE original: %.4f' % orig_mae)
    print('MAE test set: %.4f' % mae)

    # n_estimators = len(pipeline.named_steps['gbm'].estimators_)
    #
    # def deviance_plot(est, X_test, y_test, ax=None, label='', train_color='#2c7bb6',
    #                   test_color='#d7191c', alpha=1.0):
    #     """Deviance plot for ``est``, use ``X_test`` and ``y_test`` for test error. """
    #     test_dev = np.empty(n_estimators)
    #
    #     for i, pred in enumerate(est.staged_predict(X_test)):
    #        test_dev[i] = est.loss_(y_test, pred)
    #
    #     if ax is None:
    #         fig = plt.figure(figsize=(10, 10))
    #         ax = plt.gca()
    #
    #     ax.plot(np.arange(n_estimators) + 1, est.train_score_, color=train_color,
    #              label='Train %s' % label, linewidth=2, alpha=alpha)
    #     ax.plot(np.arange(n_estimators) + 1, test_dev, color=test_color, label='Test %s' % label,
    #              linewidth=2, alpha=alpha)
    #     ax.set_ylabel('Error')
    #     ax.set_xlabel('n_estimators')
    #     return test_dev, ax
    #
    # test_dev, ax = deviance_plot(pipeline.named_steps['gbm'], X_test, y_test)
    # ax.legend(loc='upper right')
    # cwd = os.getcwd()
    # plt.savefig(join(cwd, '/figures/deviance.png'))
    #
    # feature_importance = pipeline.named_steps['gbm'].feature_importances_
    # # make importances relative to max importance
    # feature_importance = 100.0 * (feature_importance / feature_importance.max())
    # sorted_idx = np.argsort(feature_importance)
    # pos = np.arange(sorted_idx.shape[0]) + .5
    # plt.figure(figsize=(20, 20))
    # plt.subplot(1, 2, 2)
    # plt.barh(pos, feature_importance[sorted_idx], align='center')
    # plt.yticks(pos, X_train.columns[sorted_idx])
    # plt.xlabel('Relative Importance')
    # plt.title('Variable Importance')
    # plt.savefig(join(cwd, '/figures/feature_importance.png'))

    submission_y = pipeline.predict(drivers.Xs['x_scoring'])

    submission_nonpivoted = pd.DataFrame({
        "ParcelId": drivers.scoring_driver["parcelid"],
        "transactiondate": drivers.scoring_driver["transactiondate"],
        "Pred": submission_y
    })

    submission = submission_nonpivoted.pivot(index='ParcelId', columns='transactiondate', values='Pred').reset_index()
    submission.columns = ['ParcelID', '201610', '201611', '201612', '201710', '201711', '201712']
    submission.to_csv(join(cwd, 'submission.csv'), index=False)

if __name__ == "__main__":
    main()
