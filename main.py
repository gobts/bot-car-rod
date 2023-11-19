import pandas as pd
import numpy as npy
from pylab import mpl, plt
import matplotlib as plotLib
import yfinance as yf
yf.pdr_override()

enterPoint = 1

simbol = 'AAPL'
startDate = '2020-01-01'
endDate = '2021-01-01'

financeData = yf.download(simbol, startDate, endDate)
EMA7 = 9
EMA21 = 200

# financeData.plot(figsize = (11, 7)).show()
def preprocessing_yf(symbol):

  # Importar los datos
  df = yf.download(symbol).dropna()

  # Renombrar las columnas
  df.columns = ["open", "high", "low", "close", "adj close", "volume"]
  df.index.name = "time"

  # Eliminar la columna adj close
  del df["adj close"]

  return df

df = preprocessing_yf("BTC")
# df = preprocessing_yf("EURUSD=X")
# df = preprocessing_yf(simbol)



# Crear media móvil simple con periodo de 30 días
df["SMA fast"] = df["close"].rolling(EMA7).mean()

# Crear media móvil simple con periodo de 60 días
df["SMA slow"] = df["close"].rolling(EMA21).mean()

# Crear la condición
# condition_buy = (df["SMA fast"] > df["SMA slow"]) & (df["SMA fast"].shift(1) < df["SMA slow"].shift(1))
condition_buy = (df["SMA fast"] > df["SMA slow"]) & (df["SMA fast"].shift(enterPoint) < df["SMA slow"].shift(enterPoint))
                
# condition_sell = (df["SMA fast"] < df["SMA slow"]) & (df["SMA fast"].shift(1) > df["SMA slow"].shift(1))
condition_sell = (df["SMA fast"] < df["SMA slow"]) & (df["SMA fast"].shift(enterPoint) > df["SMA slow"].shift(enterPoint))

df.loc[condition_buy, "signal"] = 1
df.loc[condition_sell, "signal"] = -1

#######
year = "2022"

# Seleccionar toda la señal en una lista de índices para trazar sólo estos puntos
idx_open = df.loc[df["signal"] == 1].loc[year].index
idx_close = df.loc[df["signal"] == -1].loc[year].index

# Adaptar el tamaño de la figura
plt.figure(figsize=(15,6))

# Trazar los puntos de la señal larga abierta en verde y de venta en rojo
plt.scatter(idx_open, df.loc[idx_open]["close"].loc[year], 
            color= "#57CE95", marker="^")
plt.scatter(idx_close, df.loc[idx_close]["close"].loc[year],  
            color= "red", marker="v")

# Trazar la resistencia para asegurarte de que se cumplen las condiciones
plt.plot(df["close"].loc[year].index, df["close"].loc[year], alpha=0.35)
plt.plot(df["close"].loc[year].index, df["SMA fast"].loc[year], alpha=0.35)
plt.plot(df["close"].loc[year].index, df["SMA slow"].loc[year], alpha=0.35)

# Mostrar el gráfico
plt.show()




# financeData['EMA7'] = financeData['Close'].rolling(EMA7).mean()
# financeData['EMA21'] = financeData['Close'].rolling(EMA21).mean()
# financeData.dropna(inplace = True)


# import numpy as np
# import pandas as pd
# import datetime as dt

# from pylab import mpl, plt

# from pandas_datareader import data as pdr
# !pip install yfinance
# import yfinance as yf
# yf.pdr_override()