from sklearn import preprocessing, metrics
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import scale
from sklearn.pipeline import Pipeline
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import Ridge
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV

import sys
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import Ridge
# import mord.multiclass
import pandas as pd
import numpy as np
import math
from datetime import datetime
from ord.mord import multiclass,regression_based,threshold_based


class Custom_Ridge(Ridge):
    def __init__(self, alpha=1.0, fit_intercept=True, normalize=False,
                 copy_X=True, max_iter=None, tol=1e-3, solver="auto",
                 random_state=None):
        super(Custom_Ridge, self).__init__(alpha=alpha, fit_intercept=fit_intercept,
                                    normalize=normalize, copy_X=copy_X,
                                    max_iter=max_iter, tol=tol, solver=solver,
                                    random_state=random_state)

    def score(self, X, y, sample_weight=None):
        y_t = y
        y_p = self.predict(X)
        r,c = y_t.shape
        J = y_p - y_t
        loss = np.divide(J,y_t)
        meanLoss = np.sum(np.square(loss))/r
        return meanLoss


def testscore(y_t, y_p, sample_weight=None):
    r,c = y_t.shape
    J = y_p - y_t
    loss = np.divide(J,y_t)
    meanLoss = np.sum(np.square(loss))/r
    return meanLoss


def main():
    dm = pd.read_csv("DesignMatrix", sep=',')
    salary_bins = dm['Salary']
    bins = pd.qcut(salary_bins, [0, .20, .4, .60, .8, 1.],labels=[1,2,3,4,5])
    dm['Salary'] = bins
    dm.to_csv("DesignMatrixClassification")

    inputFrame = pd.read_csv("DesignMatrixClassification")
    # print inputFrame.tail()
    inputmat = inputFrame.as_matrix()
    X = inputmat[:,1:-1]
    Y = inputmat[:,-1:]
    '''
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size =500, random_state=5)
    X_scaled = scale(X)
    scaler = StandardScaler().fit(X)
    X_trans = scaler.transform(X)
    '''

    clf2 = threshold_based.LogisticAT(alpha=1.)
    tempy = np.ndarray.flatten(Y)
    tempy = tempy.astype(int)

    clf2.fit(X, tempy)
    print('Mean Absolute Error of LogisticAT %s' %
    metrics.mean_absolute_error(clf2.predict(X), tempy))

    clf3 = threshold_based.LogisticIT(alpha=1.)
    clf3.fit(X, tempy)
    print('Mean Absolute Error of LogisticIT %s' %
    metrics.mean_absolute_error(clf3.predict(X), tempy))

    clf4 = threshold_based.LogisticSE(alpha=1.)
    clf4.fit(X, tempy)
    print('Mean Absolute Error of LogisticSE %s' %
    metrics.mean_absolute_error(clf4.predict(X), tempy))






    """pipe = Pipeline([
        ('preprocessing', StandardScaler()),
        ('custom_ridge', Custom_Ridge()),
    ])

    parameters = {
        'custom_ridge__alpha': (0.00001, 0.001, 0.001, 0.01, 0.1, 1.0, 10, 100, 1000, 100000 ),
        'custom_ridge__max_iter': (10, 100, 1000, 10000),
    }

    pipe.set_params(custom_ridge__alpha = 1.0, custom_ridge__max_iter = 100)
    pipe.fit(X,Y)
    ypredict = pipe.predict(X)
    print testscore(Y,ypredict)
    print pipe.score(X,Y)"""


    # grid_search = GridSearchCV(pipe, parameters, n_jobs=-1, verbose=1)

    # gr = grid_search.fit(X, Y)

    # print gr.best_params_

    # print gr.best_score_

    # pipe.set_params(preprocessing__with_mean=True,preprocessing__with_std=True,custom_ridge__alpha=0.0000001).fit(X,Y)
    #
    # prediction = pipe.predict(X)
    #
    # pipe.score(X,Y)
    #
    # pipe = Pipeline([
    #     ('preprocessing', StandardScaler()),
    #     ('ridge', Ridge()),
    # ])
    #
    # pipe.set_params(preprocessing__with_mean=True,preprocessing__with_std=True,ridge__alpha=10).fit(X,Y)



    # prediction = pipe.predict(X)
    # pipe.score(X,Y)



if __name__ == "__main__":
    main()