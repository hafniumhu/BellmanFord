import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from fbprophet import Prophet

df = pd.read_csv('Japantest.csv')
# delete rows without values
df = df[np.isfinite(df['y'])]
#print(df.head(7))
#a = np.array(df['Date'])
#print(a)
#prophet

m = Prophet()
m.fit(df)
future = m.make_future_dataframe(periods=7)
future.tail()
forecast = m.predict(future)
forecast[['ds','yhat','yhat_lower','yhat_upper']].tail()
fig1 = m.plot(forecast)
fig2 = m.plot_components(forecast)
plt.show()