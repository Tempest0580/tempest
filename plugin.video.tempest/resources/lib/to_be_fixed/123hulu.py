'''
    Tempest Add-on
    Copyright (C) 2016 Tempest

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
import sys
import bs4 as bs
import cfscrape
import re
import time
from bs4 import BeautifulSoup as s
from resources.lib.modules import cleantitle


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['123hulu.unblockall.org']
        self.base_link = 'http://123hulu.unblockall.org'
        self.movies_search_path = 'search-movies/%s.html'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(title).replace(' ', '-')
            url = self.base_link + self.movies_search_path + clean_title
            scraper = cfscrape.create_scraper()
            r = scraper.get(url)
            r = s(r.text, 'html.parser').find_all('div', class_="ml-item")[0]
            link = r.find_all('a')

            for i in link:
                return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(tvshowtitle).replace(' ', '-')
            url = self.base_link + self.movies_search_path + clean_title
            scraper = cfscrape.create_scraper()
            r = scraper.get(url)
            r = s(r.text, 'html.parser').find_all('div', class_="ml-item")[0]
            link = r.find_all('a')

            for i in link:
                return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        return

    def sources(self, url, hostDict, hostprDict):
        pass