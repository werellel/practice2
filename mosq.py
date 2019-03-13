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

csv_mosq_2011 = pd.read_csv('/Users/hogeunryu/Desktop/ipython/2011.csv')
csv_mosq_2012 = pd.read_csv('/Users/hogeunryu/Desktop/ipython/2012.csv')
csv_mosq_2013 = pd.read_csv('/Users/hogeunryu/Desktop/ipython/2013.csv')
csv_mosq_2014 = pd.read_csv('/Users/hogeunryu/Desktop/ipython/2014.csv')

# print(csv_mosq_2011.index)

# print(csv_mosq_2011.head())

# print(csv_mosq_2011.columns)

result = pd.concat([csv_mosq_2011, csv_mosq_2012, csv_mosq_2013, csv_mosq_2014], ignore_index=True)
print(result.info)
print(result.columns)
print(result.Mosq[0])
print(result.Date[0])

R_Date = []
for R in result.Date.tolist():
	results = re.sub(r" (\d{2}):(\d{2}):(\d{2})",
	                r"",
	                R)
	R_Date.append(results)
print("append")
print(R_Date)
print("append")

dates = pd.date_range('20110101',periods=1826)

Dic = {}
for i in range(len(R_Date)):
	Dic[R_Date[i]] = result.Mosq[i]
# print(Dic)
s = pd.Series(Dic)
s.index = pd.DatetimeIndex(s.index)
s = s.reindex(dates, fill_value=np.nan)
print(len(s))
s.to_csv('M_Data.csv', index=True, encoding='utf-8')

print(s.loc['20110501':'20110531'])
print(s.loc['20110601':'20110630'])
print(s.loc['20110701':'20110731'])
print(s.loc['20110801':'20110831'])
s.fillna(0)

s[s>9999] = np.nan

missingDataMon = [201105,201205,201206,201210,201306,201307,201308,201309,201310,201312,201406, 201409, 201411]

for S in missingDataMon:
	df = pd.DataFrame({'Date': [S] })
	df['BeginOfMonth'] = pd.to_datetime(df['Date'], format="%Y%m") + MonthBegin(0)
	df['EndOfMonth'] = pd.to_datetime(df['Date'], format="%Y%m") + MonthEnd(1)

	BeginOfMonth = str(df['BeginOfMonth'][0])
	EndOfMonth = str(df['EndOfMonth'][0])

	BeginOfMonthSTR = re.sub(r" (\d{2}):(\d{2}):(\d{2})", r"", BeginOfMonth)
	EndOfMonthSTR = re.sub(r" (\d{2}):(\d{2}):(\d{2})", r"", EndOfMonth)
	print(BeginOfMonthSTR)
	print(EndOfMonthSTR)
	s.update(s.loc[BeginOfMonthSTR:EndOfMonthSTR].fillna(math.ceil(s.loc[BeginOfMonthSTR:EndOfMonthSTR].mean()))) 
	print(s.loc[BeginOfMonthSTR:EndOfMonthSTR])
# s.to_csv('M_Data_Imputation.csv', index=True, encoding='utf-8')

s[s>1000] = 1000

s.to_csv('M_Data_Imputation.csv', index=True, encoding='utf-8')
X_Data = DataFrame.from_csv('/Users/hogeunryu/Desktop/ipython/X_Data.csv')

X_Data['Mosq'] = s.values

print(s.all)
print(X_Data)
X_Data.to_csv('X_Data_Mosq.csv', index=True, encoding='utf-8')

Hum1 = np.around(X_Data['Hum'].rolling(min_periods=1, window=1).sum(), decimals=2)
Hum2 = np.around(X_Data['Hum'].rolling(min_periods=2, window=2).sum(), decimals=2)
Hum3 = np.around(X_Data['Hum'].rolling(min_periods=3, window=3).sum(), decimals=2)
Hum4 = np.around(X_Data['Hum'].rolling(min_periods=4, window=4).sum(), decimals=2)
Hum5 = np.around(X_Data['Hum'].rolling(min_periods=5, window=5).sum(), decimals=2)
Hum6 = np.around(X_Data['Hum'].rolling(min_periods=6, window=6).sum(), decimals=2)
Hum7 = np.around(X_Data['Hum'].rolling(min_periods=7, window=7).sum(), decimals=2)
Hum8 = np.around(X_Data['Hum'].rolling(min_periods=8, window=8).sum(), decimals=2)


Hum5 = np.around(X_Data['Hum'].rolling(min_periods=5, window=5).sum(), decimals=2)
Raf6 = np.around(X_Data['Raf'].rolling(min_periods=1, window=6).sum(), decimals=2)
Tav16 = np.around(X_Data['Tav'].rolling(min_periods=16, window=16).sum(), decimals=2)
Tmi2 = np.around(X_Data['Tmi'].rolling(min_periods=2, window=2).sum(), decimals=2)
Tmx19 = np.around(X_Data['Tmx'].rolling(min_periods=19, window=19).sum(), decimals=2)
# X_Data['Location'] = "YangPyung"
# X_Data['Date'] = dates

X_DatTF = X_Data['Raf'].copy(deep=True)
X_Data['Rfd29'] = X_DatTF.values
X_Data['Rfd29'][X_Data['Rfd29'].values > 0] = 1

X_Data['Raf'] = X_DatTF.values
Rfd29 = np.around(X_Data['Rfd29'].rolling(min_periods=29, window=29).sum(), decimals=2)
X_Data['Hum5'] = Hum5
X_Data['Raf6'] = Raf6
X_Data.to_csv('Raf6.csv', index=True, encoding='utf-8')
X_Data['Tav16'] = Tav16
X_Data['Tmi2'] = Tmi2
X_Data['Tmx19'] = Tmx19
X_Data['Rfd29'] = Rfd29

X_Data['LandUse'] = 3

# X_Data.to_csv('X_Data_Mosq_Final.csv', index=True, encoding='utf-8')
# print(np.math.log(s.values/10, 2))
Level = []
# print((np.ceil(np.log2(s.values/10))))
for val in s.values:
	if val == "nan":
		a = val
	else:
		a, b = divmod(val, 20)
		if not b == 0:
			a += 1
	if a == -0.0:
		a = 0.0
	Level.append(a)

# print(Level)

# MD = pd.Series(np.ceil(np.log2(s.values/10)))
X_Data['Level'] = Level
X_Data.drop('Mosq', axis=1, inplace=True)
X_Data.to_csv('X_Data_Mosq_Final.csv', index=True, encoding='utf-8')
# print(X_Data['Rfd29'].values)

X_Data.drop('Hum', axis=1, inplace=True)
X_Data.drop('Raf', axis=1, inplace=True)
X_Data.drop('Tav', axis=1, inplace=True)
X_Data.drop('Tmi', axis=1, inplace=True)
X_Data.drop('Tmx', axis=1, inplace=True)
X_Data.to_csv('Data_F.csv', index=True, encoding='utf-8')
# X_Data.drop(X_Data['Level']['nan'], inplace=True)
X_Data.dropna(inplace=True) 
X_Data.to_csv('Data.csv', index=True, encoding='utf-8')

# print(X_Data)
# print(X_Data)
# for i in range(31):
# 	i += 1
# 	print(s.get("2011-05-%d" % i))
# 	Max += s.get("2011-05-%d" % i)
# print(Max)
# AVG = Max / 31
# AVG2 = math.ceil(AVG)
# print(AVG2)
# for i in range(31):
# 	i += 1
# 	val = s.get("2011-05-%d" % i)
# 	print("2011-05-%d" % i)
# 	print(int(val))
# 	print("val")
# 	if int(val) == 0:
# 		s.set_value(s.get("2011-05-%d" % i), AVG2)
# 	else:
# 		print("good")


# print(s)
# print(date_str_list[0])
# print()
# for date in result.Date:





# df = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB')