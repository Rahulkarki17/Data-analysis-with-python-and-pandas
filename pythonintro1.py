import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import datetime
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')

start = datetime.datetime(2010, 1, 1)
end = datetime.datetime.now()

df = web.DataReader("F", "robinhood", start, end)

df.reset_index(inplace=True)
df.set_index("begins_at", inplace=True)
df = df.drop("symbol", axis=1)

print(df.head())

df['high_price'].plot()
plt.legend()
plt.show()

