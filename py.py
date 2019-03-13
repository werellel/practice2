from bs4 import BeautifulSoup
import math
from math import ceil
from math import log2
import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas.tseries.offsets import MonthBegin
from pandas.tseries.offsets import MonthEnd

import re
import requests

import urllib
from json import dumps

try:
    from urllib import urlencode, unquote
    from urlparse import urlparse, parse_qsl, ParseResult
except ImportError:
    # Python 3 fallback
    from urllib.parse import (
        urlencode, unquote, urlparse, parse_qsl, ParseResult
    )


Tav = [25.3,24.3,24.7,26.7,27.4,27.6,26.4,26.0,26.3,24.0,26.0,27.1,27.6,28.7,25.0,26.2,26.8,26.5,28.3,29.9,29.8,29.3,27.0,26.2,29.4,28.7,27.1,25.5,27.2,27.9,25.7,28.6,30.0,30.2,30.3,31.4,29.8,29.2,28.2,27.6,24.8,27.0,27.8,26.3,24.6,21.9,23.3,24.8,26.3,26.1,23.2,25.8,27.3,27.2,26.5,25.3,24.2,22.7,21.5,19.5,19.8,22.2]
Tmx = [30.7,26.8,27.4,31.6,32.6,34.6,28.4,27.6,30.3,25.4,30.9,31.1,32.1,33.0,27.3,28.8,29.0,30.7,34.1,34.9,32.4,32.5,28.1,27.3,35.4,32.8,29.7,26.9,30.1,32.6,27.1,33.0,33.0,33.9,35.3,34.8,34.0,34.4,31.0,32.0,26.3,32.4,32.6,28.4,27.1,24.0,26.8,27.7,30.6,28.7,25.8,29.2,31.5,30.2,28.1,30.6,29.2,26.7,26.5,24.0,23.9,27.6]
Tmi = [22.4,21.9,21.9,23.8,23.3,23.9,24.4,24.6,23.8,22.6,22.2,24.9,23.1,26.1,23.4,23.4,24.0,23.9,24.5,26.0,27.3,27.5,26.1,25.6,24.6,24.2,24.9,24.8,25.0,24.7,24.8,24.1,26.6,27.2,25.9,27.6,28.2,26.4,25.5,24.6,23.9,23.9,23.2,24.2,23.1,20.8,20.5,21.2,23.9,23.1,22.0,23.7,23.4,24.6,23.9,22.2,19.0,19.0,18.3,17.0,16.1,16.6]
Hum = [73.6,90.5,87.6,74.5,66.9,72.3,80.8,83.3,88.0,96.5,81.4,75.9,71.0,68.4,89.0,83.4,77.3,80.6,71.4,66.1,73.1,75.8,89.5,82.3,64.1,55.6,62.5,92.1,72.3,64.4,82.3,73.0,71.9,60.6,60.1,63.0,71.9,68.1,67.1,66.4,89.9,72.5,60.3,62.1,67.5,93.8,80.5,77.1,75.6,75.8,95.6,81.5,70.6,84.1,85.3,61.9,54.5,62.0,73.1,51.4,55.8,62.4]
Raf = [0.5,92.0,67.5,0.5,0.0,34.0,16.5,4.5,32.5,144.5,1.0,0.0,0.0,0.0,42.5,22.5,7.5,2.5,0.0,0.0,0.0,0.5,133.5,3.0,0.0,0.0,3.5,8.5,0.0,0.0,3.5,2.0,0.0,0.0,0.0,0.0,5.0,0.0,0.0,2.5,5.5,0.5,0.0,0.0,1.5,93.5,2.0,0.5,0.0,0.0,124.5,5.0,0.0,31.5,14.0,0.0,0.0,0.0,9.0,0.0,0.0,0.0]	 	 	 
dates = pd.date_range('20170701',periods=62)
print(len(Tav))
print(len(Tmx))
print(len(Tmi))
print(len(Hum))
print(len(Raf))

X_Data = pd.DataFrame({'Tav' : Tav, 'Tmx': Tmx, 'Tmi': Tmi, 'Hum': Hum, 'Raf': Raf}, index = dates)
print(X_Data)
Hum5 = np.around(X_Data['Hum'].rolling(min_periods=5, window=5).sum(), decimals=2)
Raf6 = np.around(X_Data['Raf'].rolling(min_periods=1, window=6).sum(), decimals=2)
Tav16 = np.around(X_Data['Tav'].rolling(min_periods=16, window=16).sum(), decimals=2)
Tmi2 = np.around(X_Data['Tmi'].rolling(min_periods=2, window=2).sum(), decimals=2)
Tmx19 = np.around(X_Data['Tmx'].rolling(min_periods=1, window=19).sum(), decimals=2)

X_DatTF = X_Data['Raf'].copy(deep=True)
X_Data['Rfd29'] = X_DatTF.values
X_Data['Rfd29'][X_Data['Rfd29'].values > 0] = 1

X_Data['Raf'] = X_DatTF.values
Rfd29 = np.around(X_Data['Rfd29'].rolling(min_periods=29, window=29).sum(), decimals=2)
X_Data['Hum5'] = Hum5
X_Data['Raf6'] = Raf6

X_Data['Tav16'] = Tav16
X_Data['Tmi2'] = Tmi2
X_Data['Tmx19'] = Tmx19
X_Data['Rfd29'] = Rfd29
X_Data['LandUse'] = 3
X_Data.to_csv('2017_Raf6.csv', index=True, encoding='utf-8')
X_Data.dropna(inplace=True) 
# MD = pd.Series(np.ceil(np.log2(s.values/10)))
X_Data['Level'] = np.nan
# X_Data.drop('Mosq', axis=1, inplace=True)
X_Data.to_csv('2017_X_Data_Mosq_Final.csv', index=True, encoding='utf-8')
# print(X_Data['Rfd29'].values)

X_Data.drop('Hum', axis=1, inplace=True)
X_Data.drop('Raf', axis=1, inplace=True)
X_Data.drop('Tav', axis=1, inplace=True)
X_Data.drop('Tmi', axis=1, inplace=True)
X_Data.drop('Tmx', axis=1, inplace=True)
X_Data.to_csv('2017_Data_F.csv', index=True, encoding='utf-8')
# X_Data.drop(X_Data['Level']['nan'], inplace=True)
# X_Data.dropna(inplace=True) 
X_Data.to_csv('2017_Data.csv', index=True, encoding='utf-8')
