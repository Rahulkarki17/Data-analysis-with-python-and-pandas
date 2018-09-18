import pandas as pd
import datetime
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web

start = datetime.datetime(2010, 1, 1)
end = datetime.datetime.now()

df = web.DataReader("XOM", "morningstar", start, end)

print(df)
