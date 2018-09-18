##Rolling - window of time 

import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')


#Not necessary - This just hides your API key.
api_key = 'mojsgxGvDAeUtRh8BX-H'

def state_list():
    fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return fiddy_states[0][1][1:]

def grab_initial_state_data():
    states = state_list()
    main_df = pd.DataFrame()

    #print(fiddy_states[0][1])
    for abbv in states:
        #print(abbv)
        query = "FMAC/HPI_"+str(abbv)
        #print(query)
        df = quandl.get(query, authtoken=api_key)
        df.columns=[abbv]
        df[abbv] = (df[abbv]-df[abbv][0]) / df[abbv][0]* 100.0
        print(df.head())
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)


    pickle_out = open('fiddy_states3.pickle', 'wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()

def HPI_Benchmark():
    df = quandl.get("FMAC/HPI_USA", authtoken=api_key)
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    return df

    
###grab_initial_state_data()

fig = plt.figure()
ax1 = plt.subplot2grid((2,1), (0,0))
ax2 = plt.subplot2grid((2,1), (1,0), sharex=ax1)

HPI_data = pd.read_pickle('fiddy_states3.pickle')
##HPI_data['TX12MA'] = HPI_data['TX'].rolling(12).mean()
##HPI_data['TX12STD'] = HPI_data['TX'].rolling(12).std()
##print(HPI_data[['TX','TX12MA', 'TX12STD']].head())
##
##HPI_data[['TX','TX12MA']].plot(ax = ax1)
##HPI_data['TX12STD'].plot(ax=ax2)


TX_AK_12corr = HPI_data['TX'].rolling(window=12).corr(HPI_data['AK'])

HPI_data['TX'].plot(ax=ax1, label= 'TX HPI')
HPI_data['AK'].plot(ax=ax1, label= 'AK HPI')
ax1.legend(loc=4)

TX_AK_12corr.plot(ax=ax2, label='TX_AK_12corr')


plt.legend(loc = 4 )
plt.show()

###Options for Handling missing DATA
#Ignore it
#Delete it
#fill forwards or backwards
#Replace it with something static

#1Dropna - Drops the NaN values - notice that this samples vlaues every year*** compared to montly
#2Dropna - but only rows that have all NaN - HPI_data.dropna(how='all', inplace=True)
#3Fillna - forward fill 'ffill' or backward 'bfill' or add raw value f -99999 (used in machine learning)




