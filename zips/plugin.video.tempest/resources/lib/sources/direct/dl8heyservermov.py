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
        self.domains = ['dl8.heyserver.in']
        self.base_link = 'http://dl8.heyserver.in/film/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.get_query(title)
            self.title = '%s.%s' % (title, year)
            url = self.base_link
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            title = self.title
            result = url
            r = requests.get(result, timeout=10).content
            r = re.compile('a href="(.+?)"').findall(r)
            for r in r:
                if '2018-10/' in r:
                    result2 = result + '2018-10/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not title in url:
                            continue
                        if 'Dubbed' in url:
                            continue
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'Direct', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                elif '2018-11/' in r:
                    result2 = result + '2018-11/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not title in url:
                            continue
                        if 'Dubbed' in url:
                            continue
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'Direct', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                elif '2018-12/' in r:
                    result2 = result + '2018-12/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not title in url:
                            continue
                        if 'Dubbed' in url:
                            continue
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'Direct', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                elif '2018-3/' in r:
                    result2 = result + '2018-3/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not title in url:
                            continue
                        if 'Dubbed' in url:
                            continue
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'Direct', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                elif '2018-4/' in r:
                    result2 = result + '2018-4/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not title in url:
                            continue
                        if 'Dubbed' in url:
                            continue
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'Direct', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                elif '2018-5/' in r:
                    result2 = result + '2018-5/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not title in url:
                            continue
                        if 'Dubbed' in url:
                            continue
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'Direct', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                elif '2018-6/' in r:
                    result2 = result + '2018-6/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not title in url:
                            continue
                        if 'Dubbed' in url:
                            continue
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'Direct', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                elif '2018-7/' in r:
                    result2 = result + '2018-7/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not title in url:
                            continue
                        if 'Dubbed' in url:
                            continue
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'Direct', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                elif '2018-8/' in r:
                    result2 = result + '2018-8/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not title in url:
                            continue
                        if 'Dubbed' in url:
                            continue
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'Direct', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                elif '2018-9/' in r:
                    result2 = result + '2018-9/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not title in url:
                            continue
                        if 'Dubbed' in url:
                            continue
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'Direct', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                else:
                    result2 = result + '2019-1/'
                    r = requests.get(result2, timeout=10).content
                    r = re.compile('a href="(.+?)"').findall(r)
                    for url in r:
                        if not title in url:
                            continue
                        if 'Dubbed' in url:
                            continue
                        url = result2 + url
                        quality = source_utils.check_direct_url(url)
                        sources.append({'source': 'Direct', 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return

    def resolve(self, url):
        return url
