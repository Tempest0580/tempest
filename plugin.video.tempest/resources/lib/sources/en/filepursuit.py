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
import sys
import re
from bs4 import BeautifulSoup
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:

    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domain = 'filepursuit.com'
        self.search_link = 'https://filepursuit.com/search3/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'title': title, 'year': year}
            return url
        except:
            return url

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = tvshowtitle.replace(' ', '-')
        except:
            return url
        return url

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if len(episode) == 1: episode = "0" + episode
            if len(season) == 1: season = "0" + season
            url = {'tvshowtitle': url, 'season': season, 'episode': episode}
            return url
        except:
            return url

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            with requests.Session() as s:
                if 'episode' in url:
                    link = cleantitle.query(url['tvshowtitle']) + ".s" + url['season'] + "e" + url['episode']
                else:
                    link = cleantitle.query("%s.%s") % (url['title'], url['year'])
                p = s.get(self.search_link + link + "/type/videos")
                soup = BeautifulSoup(p.text, 'html.parser').find_all('table')[0]
                soup = soup.find_all('button')
                for i in soup:
                    url = i['data-clipboard-text']
                    source_check = url.lower(), re.sub('[^0-9a-zA-Z]+', '.', link).lower()
                    if source_check  != False:
                        hoster = url.split('/')[2]
                        quality = source_utils.check_sd_url(url)
                        sources.append({
                            'source': hoster, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False,
                        })
            return sources

        except:
            return sources

    def resolve(self, url):
        return url
