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

import re

from resources.lib.modules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['odb.to']
        self.base_link = 'https://api.odb.to'
        self.movie_link = '/embed?imdb_id=%s'
        self.tv_link = '/embed?imdb_id=%s&s=%s&e=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.base_link + self.movie_link % imdb
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = imdb
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url: return
            imdb = url
            url = self.base_link + self.tv_link % (imdb, season, episode)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = client.request(url)
            try:
                match = re.compile('<iframe src="(.+?)" width').findall(r)
                for url in match:
                    host = url.replace('https://', '').replace('http://', '').replace('www.', '')
                    sources.append({
                        'source': host,
                        'quality': 'HD',
                        'language': 'en',
                        'url': url,
                        'direct': False,
                        'debridonly': False
                    })
            except:
                return
        except Exception:
            return
        return sources

    def resolve(self, url):
        return url
