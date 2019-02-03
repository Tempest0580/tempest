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

import re, requests

from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['dl5.dlb3d.xyz']
        self.base_link = 'http://dl5.dlb3d.xyz/'
        self.search_link = 'Movies/%s/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.get_query(title)
            self.title = '%s.%s' % (title, year)
            self.year = year
            url = self.base_link + self.search_link % self.title
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = requests.get(url, timeout=10).content
            r = re.compile('a href="(.+?)"').findall(r)
            for u in r:
                if not self.title in u:
                    continue
                if 'Trailer' in u:
                    continue
                if 'Dubbed' in u:
                    continue
                if 'rar' in u:
                    continue
                url = self.base_link + self.search_link % self.title + u
                quality = source_utils.check_url(url)
                sources.append({'source': 'Direct', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
            return sources
        except:
            return

    def resolve(self, url):
        return url
