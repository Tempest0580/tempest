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
        self.domains = ['dl2.dldrm.ir']
        self.base_link = 'http://dl2.dlb3d.xyz/S/'
        self.search_link = '%s/'

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            title = cleantitle.get_query(tvshowtitle)
            title = '%s' % title.replace('.', '%20')
            url = self.base_link + self.search_link % title
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            self.se = 'S%02dE%02d' % (int(season), int(episode))
            season = 'S%02d/' % int(season)
            if not url: return
            url = url + season
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            se = self.se
            result = url
            r = requests.get(result, timeout=10).content
            r = re.findall('a href=".+?">(.+?)<', r)
            for r in r:
                if not se in r:
                    continue
                if 'Trailer' in r:
                    continue
                url = result + r
                quality = source_utils.check_direct_url(url)
                sources.append({'source': 'Direct', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return

    def resolve(self, url):
        return url
