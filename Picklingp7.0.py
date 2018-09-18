import quandl
import pandas as pd
import pickle

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
        #print(df.head())
        

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df)
    print(main_df.head())

    pickle_out = open('fiddy_states.pickle', 'wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()

#grab_initial_state_data()

pickle_in = open('fiddy_states.pickle','rb')
HPI_data = pickle.load(pickle_in)
#print(HPI_data)

HPI_data.to_pickle('pickle.pickle')
HPI_data2 = pd.read_pickle('pickle.pickle')
print(HPI_data2)

