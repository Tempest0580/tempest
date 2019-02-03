# -*- coding: utf-8 -*-

'''
    Tempest Add-on
    **Created by Tempest**

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

import re

from resources.lib.modules import source_utils
from resources.lib.modules import cleantitle
from resources.lib.modules import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['spacemov.cc']
        self.base_link = 'https://spacemov.cc'
        self.search_link = '/search-query/%s+%s/'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title).replace('-', '+')
            r = self.base_link + self.search_link % (title, year)
            r = self.scraper.get(r).content
            url = re.findall('a href="(.+?)" class="ml-mask jt"', r)[0]
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            hostDict = hostprDict + hostDict
            url = url + 'watching/?ep=1'
            r = self.scraper.get(url).content
            r = re.compile('a title="(.+?)" data-svv.+?="(.+?)"').findall(r)
            for title, url in r:
                if 'HD' in title:
                    quality = '1080p'
                elif 'CAM' in title:
                    quality = 'CAM'
                else:
                    quality = 'SD'
                if 'vidcloud' in url:
                    r = self.scraper.get(url).content
                    t = re.findall('li data-status=".+?" data-video="(.+?)"', r)
                    for url in t:
                        if 'vidcloud' in url:
                            continue
                        valid, host = source_utils.is_host_valid(url, hostDict)
                        if valid:
                            sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                if 'vidcloud' in url:
                    continue

                valid, host = source_utils.is_host_valid(url, hostDict)
                if valid:
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return

    def resolve(self, url):
        return url
