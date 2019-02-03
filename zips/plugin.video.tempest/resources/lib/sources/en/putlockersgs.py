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
import base64
from resources.lib.modules import cleantitle
from resources.lib.modules import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['putlockers.gs', '0123putlocker.com']
        self.base_link = 'http://www1.putlockers.gs'
        self.search_link = '/search-movies/%s.html'
        self.scraper = cfscrape.create_scraper()

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            url = url.replace('-', '+')
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url: return
            query = url + '+season+' + season
            find = query.replace('+', '-')
            url = self.base_link + self.search_link % query
            r = self.scraper.get(url).content
            match = re.compile('<a href="http://putlockers.gs/watch/(.+?)-' + find + '.html"').findall(r)
            for url_id in match:
                url = 'http://putlockers.gs/watch/' + url_id + '-' + find + '.html'
                r = self.scraper.get(url).content
                match = re.compile('<a class="episode episode_series_link" href="(.+?)">' + episode + '</a>').findall(r)
                for url in match:
                    return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = self.scraper.get(url).content
            try:
                match = re.compile(
                    '<p class="server_version"><img src="http://putlockers.gs/themes/movies/img/icon/server/(.+?).png" width="16" height="16" /> <a href="(.+?)">').findall(
                    r)
                for host, url in match:
                    if host == 'internet':
                        pass
                    else:
                        sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False,
                                        'debridonly': False})
            except:
                return
        except Exception:
            return
        return sources

    def resolve(self, url):
        r = self.scraper.get(url).content
        match = re.compile('decode\("(.+?)"').findall(r)
        for info in match:
            info = base64.b64decode(info)
            match = re.compile('src="(.+?)"').findall(info)
            for url in match:
                return url
