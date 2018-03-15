# -*- coding: UTF-8 -*-

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
import cfscrape
import traceback
from bs4 import BeautifulSoup as bs


#from resources.lib.modules import debrid
#from resources.lib.modules import source_utils
from resources.lib.modules import log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['crazy4tv.com', 'crazy4ad.in']
        self.base_link = 'http://crazy4tv.com'
        self.search_link = '/search/arrow s06e14'

    def sources(self):
        try:
            sources = []
            url = self.base_link + self.search_link.replace(' ', '+')
            scraper = cfscrape.create_scraper()
            r = scraper.get(url).text
            r = bs(r, 'html.parser')
            link = r.findAll('strong')

            for i in link:
                s = i.findAll('a')
                for url in s:
                    host = url.text
                    url = url['href']

                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': True})
            return sources
        except:
            failure = traceback.format_exc()
            log_utils.log('A - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url

source.sources()