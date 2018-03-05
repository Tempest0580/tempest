import requests
import re
from bs4 import BeautifulSoup as bs

year = '2017'
sources = []
base_url = 'http://dl.hastidl.net/remotes/'
html = requests.get(base_url).content
soup = bs(html, 'lxml')
match = soup.find_all('a')

for url, name in match:
    if year in name:
        print base_url + url['href']