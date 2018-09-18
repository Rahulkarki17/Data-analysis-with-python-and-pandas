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
    df.rename(columns={'Value':'United States'}, inplace=True)
    df = df['United States']
    return df

def mortgage_30y():
    df = quandl.get("FMAC/MORTG", trim_start="1975-01-01", authtoken=api_key)
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0]* 100.0
    df = df.resample('D').mean()
    df = df.resample('M').mean()
    df.columns = ['M30']
    return df

def sp500_data():
    df = pd.read_csv('sp500.csv') # read the csv into a Dataframe
    df['Date']=pd.to_datetime(df['Date']) # Convert the 'Date' column to a datetime object
    df.set_index('Date', inplace=True) # set the index
    df["Adj Close"] = (df["Adj Close"]-df["Adj Close"][0]) / df["Adj Close"][0] * 100.0
    df=df.resample('M').mean()
    df.rename(columns={'Adj Close':'sp500'}, inplace=True)
    df = df['sp500']
    return df


def gdp_data():
    df = quandl.get("BCB/4385", trim_start="1975-01-01", authtoken=api_key)
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df=df.resample('M').mean()
    df.rename(columns={'Value':'GDP'}, inplace=True)
    df = df['GDP']
    return df

##def us_unemployment():
##    df = quandl.get("ECPI/JOB_G", trim_start="1975-01-01", authtoken=api_key)
##    df["Unemployment Rate"] = (df["Unemployment Rate"]-df["Unemployment Rate"][0]) / df["Unemployment Rate"][0] * 100.0
##    df=df.resample('1D').mean()
##    df=df.resample('M').mean()
##    return df
    
HPI_data = pd.read_pickle('fiddy_states3.pickle')
m30 = mortgage_30y()
sp500 = sp500_data()
gdp = gdp_data()
HPI_Bench = HPI_Benchmark()
##unemployment = us_unemployment()

#print(sp500.head())
#print(gdp.head())
##print(unemployment.head())

HPI = HPI_data.join([HPI_Bench, m30, gdp, sp500])
HPI.dropna(inplace=True)
print(HPI)
print(HPI.corr())

HPI.to_pickle('HPI.pickle')


