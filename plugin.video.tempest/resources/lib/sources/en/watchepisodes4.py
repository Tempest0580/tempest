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
import sys
from bs4 import BeautifulSoup

class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = 'watchepisodes4.com'
        self.base_link = 'http://www.watchepisodes4.com'
        self.search = '/search/ajax_search?q=%s'

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = tvshowtitle
        except:
            return url
        return url

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            url = {'tvshowtitle': url, 'season': season, 'episode': episode}
            return url
        except:
            return url

    def searchShow(self, title, season, episode):
        try:
            url = '%s/%s/season/%01d/episode/%01d' % (self.base_link, int(title), int(season), int(episode))
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        with requests.Session() as s:
            sources = []
            episode_link = 'http://www.watchepisodes4.com/arrow-season-6-episode-13-s06e13_390182'
            p = s.get(episode_link)
            soup = BeautifulSoup(p.content, 'html.parser')
            link = soup.findAll('a', class_='site-link')

            for i in link:
                if 'thevideo' in i.get('data-hostname'):
                    sources.append(
                        {'source': "speedvid", 'quality': '', 'language': "en", 'url': i.get('data-actuallink'), 'info': '',
                         'direct': False, 'debridonly': False})
                if 'openload' in i['data-host-name']:
                    sources.append(
                        {'source': "openload", 'quality': '', 'language': "en", 'url': i.get('data-actuallink'), 'info': '',
                         'direct': False, 'debridonly': False})
                if 'vshare' in i['data-hostname']:
                    sources.append(
                        {'source': "thevideo", 'quality': '', 'language': "en", 'url': i.get('data-actuallink'), 'info': '',
                         'direct': False, 'debridonly': False})
        print sources
