# -*- coding: utf-8 -*-
'''
    Tempest Add-on

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import requests
import re



from bs4 import BeautifulSoup

mozhdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}

class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = 'watchepisodes4.com'
        self.base_link = 'http://www.watchepisodes4.com'
        self.search = '/%s'

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return

            search_id = cleantitle.get(title.lower())

            url = requests.get(url)
            url = BeautifulSoup(url.content, 'html.parser')
            url = url.find_all('div', class_='el-item')
            url = re.findall(r'href="(.+?)" title="(.+?)"', str(url))

            for url, name in url:
                print url, name
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        print url


search = 'arrow'

url = 'http://www.watchepisodes4.com/%s' % search
url = requests.get(url)
url = BeautifulSoup(url.content, 'html.parser')
url = url.find_all('div', class_='el-item')
url = re.findall(r'href="(.+?)" title="(.+?)"', str(url))

for url, name in url:

    print url, name
