#Basic Machine Learning

import quandl
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from statistics import mean
from sklearn import svm, preprocessing, cross_validation

style.use('fivethirtyeight')

#Not necessary - This just hides your API key.
api_key = 'mojsgxGvDAeUtRh8BX-H'

#Calculate the difference - bigger or lesser number.
#We can do this function mapping.

def create_labels(cur_hpi, fut_hpi):
    if fut_hpi > cur_hpi:
        return 1
    else:
        return 0

def moving_average(values):
    return mean(values)


housing_data = pd.read_pickle('HPI.pickle')
housing_data = housing_data.pct_change()


#First value is NaN because we cant calculate percentage change for the first number.
#Got some -infinite values and NaN

housing_data.replace([np.inf, -np.inf], np.nan, inplace=True)
housing_data['US_HPI_future'] = housing_data['United States'].shift(-1)

housing_data.dropna(inplace=True)
#print(housing_data[['US_HPI_future', 'United States']].head())
housing_data['label'] = list(map(create_labels, housing_data['United States'], housing_data['US_HPI_future'] ))
#print(housing_data.head())

#print(housing_data.tail())

X = np.array(housing_data.drop(['label','US_HPI_future'], 1))
X = preprocessing.scale(X)
Y = np.array(housing_data['label'])

#crossvalidation - 0.2 means 20%

X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X, Y, test_size=0.2)

clf = svm.SVC(kernel='linear')
clf.fit(X_train, Y_train)

print(clf.score(X_test, Y_test))
#print(housing_data.drop(['label','US_HPI_future'], 1)

