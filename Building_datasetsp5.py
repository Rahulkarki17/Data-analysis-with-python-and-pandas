import quandl
import pandas as pd

#Not necessary - This just hides your API key.
#api_key = open('quandlapikey.txt','r').read()

df = quandl.get("FMAC/HPI_TX", authtoken='mojsgxGvDAeUtRh8BX-H')

#print(df.head())

fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
print(fiddy_states[0][1][1:])

for abbv in fiddy_states[0][1][1:]:
    #print(abbv)
    print("FMAC/HPI_"+str(abbv))
