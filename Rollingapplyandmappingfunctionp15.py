import quandl
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from statistics import mean
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

#housing_data['ma_apply_example'] = pd.rolling_apply(housing_data['M30'], 10, moving_average)
housing_data['ma_apply_example'] = housing_data['M30'].rolling(10).apply(moving_average)

print(housing_data.tail())
