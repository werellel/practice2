from bs4 import BeautifulSoup

import pandas as pd

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

def add_url_params(url, params):
    """ Add GET params to provided URL being aware of existing.

    :param url: string of target URL
    :param params: dict containing requested params to be added
    :return: string with updated URL

    >> url = 'http://stackoverflow.com/test?answers=true'
    >> new_params = {'answers': False, 'data': ['some','values']}
    >> add_url_params(url, new_params)
    'http://stackoverflow.com/test?data=some&data=values&answers=false'
    """
    # Unquoting URL first so we don't loose existing args
    url = unquote(url)
    # Extracting url info
    parsed_url = urlparse(url)
    # Extracting URL arguments from parsed URL
    get_args = parsed_url.query
    # Converting URL arguments to dict
    parsed_get_args = dict(parse_qsl(get_args))
    # Merging URL arguments dict with new params
    parsed_get_args.update(params)

    # Bool and Dict values should be converted to json-friendly values
    # you may throw this part away if you don't like it :)
    parsed_get_args.update(
        {k: dumps(v) for k, v in parsed_get_args.items()
         if isinstance(v, (bool, dict))}
    )

    # Converting URL argument to proper query string
    encoded_get_args = urlencode(parsed_get_args, doseq=True)
    # Creating new parsed result object based on provided with new
    # URL arguments. Same thing happens inside of urlparse.
    new_url = ParseResult(
        parsed_url.scheme, parsed_url.netloc, parsed_url.path,
        parsed_url.params, encoded_get_args, parsed_url.fragment
    ).geturl()

    return new_url


url = 'http://www.kma.go.kr/weather/climate/past_table.jsp?stn=108'

def loopGetURL(yy = 2017, obs = 10):
	urlsList = []
	while yy < 2018:
		# print("getURL %d" % yy)
		new_params = {'yy': yy, 'obs': obs}
		urls = add_url_params(url, new_params)
		urlsList.append(urls)
		yy = yy +1
	print("urlsList")
	print(urlsList)
	return urlsList


# print(URLList)


# # url = 'http://www.kma.go.kr/weather/climate/past_table.jsp?stn=108&yy=2013&obs=07&x=29&y=10'
# html = requests.get(url).text
# soup = BeautifulSoup(html)

# for member in soup.select('.table_develop thead tr th'):
# 	name = member.text

# 	print(name)

# for member in soup.select('.table_develop tbody tr td'):
# 	name = member.text

# 	print(name)
def name_return(index = 0):
	nameList = []
	for member in soup.select('.table_develop tbody tr'):
		name = member.select('td')
		nameList.append(name[index].text)
	return nameList

# janu = name_return() 
# del janu[31]
# while janu.count("\xa0") > 0:
# 	janu.remove("\xa0")
 	
def loopGet(index = 0, obs = 'obs'):
	getList = []
	for number in range(index):
		if number == 0:
			pass
		else:
			Get = name_return(number)
			del Get[31]
			if not obs == 21:
				while Get.count("\xa0") > 0:
					Get.remove("\xa0")
					Get
				getList.extend(Get)
			else:
				getList.extend(Get)
	print(len(getList))
	return getList




obsList = [12, 21, 10, 7, 8]
Lists = []
for obs in obsList:
	janu = []
	URLList = loopGetURL(2017, obs)
	for url in URLList:
		html = requests.get(url).text
		soup = BeautifulSoup(html)
		janu.extend(loopGet(13, obs))
	Lists.append(janu)


print(Lists[1][59])
del Lists[1][59]
print(Lists[1][59])
del Lists[1][59]
print(Lists[1][59])
del Lists[1][59]
print(Lists[1][120])
del Lists[1][120]
print(Lists[1][181])
del Lists[1][181]
print(Lists[1][273])
del Lists[1][273]
print(Lists[1][334])
del Lists[1][334]
print(len(Lists[1]))



for n,i in enumerate(Lists[1]):
	if i=="\xa0":
		Lists[1][n]=0.0

print(len(Lists[1]))
print(Lists[1])

dates = pd.date_range('20170801',periods=365)

df = pd.DataFrame({'Hum' : pd.Categorical(Lists[0]), 'Raf' : pd.Categorical(Lists[1]),'Tmi': pd.Categorical(Lists[2]), 'Tav': pd.Categorical(Lists[3]), 'Tmx': pd.Categorical(Lists[4])}, index = dates)
# df['date'] = pd.to_datatime(df['date'])
df.to_csv('2017.csv', index=True, encoding='utf-8')
print(df.head())
print(df.tail())
# janu = loopGet(13)
# print(janu)




# urls = add_url_params(url, new_params) == \
#     'http://stackoverflow.com/test/?question=%7B%22__X__%22%3A+%22__Y__%22%7D'

# del janu[31]
# while janu.count("\xa0") > 0:


# print(janu)
# print(len(janu))

# for member in soup.select('.table_develop tbody tr'):
# 		name = member.select('td')
# 		print(name[1].text)

# for member in soup.select('.table_develop tbody tr'):
# 	name = member.select('td')
# 	print(name[1])
