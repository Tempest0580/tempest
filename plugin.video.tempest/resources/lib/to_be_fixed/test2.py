import requests
from bs4 import BeautifulSoup as bs


url = 'https://watch-series.co/series/arrow-season-6'
result = url + '/season'
result = requests.get(result)
r = bs(result.text, 'html.parser')
r = r.find_all('a', class_='videoHname')

for i in r:
    print i['href']