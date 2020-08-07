# -*- coding: UTF-8 -*-
"""
    **Created by Tempest**
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""

import re, urllib, urlparse
import traceback

from resources.lib.modules import client, log_utils
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['wwv.icefilms-info.com']
        self.base_link = 'https://wwv.icefilms-info.com'
        self.headers = {'User-Agent': client.agent()}

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def searchShow(self, title, season, episode, year):
        try:
            season = 'S%01d EP%01d:' % (int(season), int(episode))
            r = '%s/search?q=%s+%s' % (self.base_link, cleantitle.geturl(title), year)
            r = client.request(r, headers=self.headers)
            r = re.compile('<a href="(.+?)">\s+<span class="title">(.+?)</span>').findall(r)
            r = [i for i in r if title in i[1] and year in i[1]][0][0]
            r = client.request(r, headers=self.headers)
            t = client.parseDOM(r, "ul", attrs={'class': 'streams'})
            for t in t:
                r = client.parseDOM(t, 'li')
                for r in r:
                    if season in r:
                        url = re.findall('<a href="(.+?)" target="_blank"><span class="hoster-title">.+?</span>', r)
                        return url
        except:
            return

    def searchMovie(self, title, year):
        try:
            r = '%s/search?q=%s+%s' % (self.base_link, cleantitle.getUrl(title), year)
            r = client.request(r, headers=self.headers)
            r = re.compile('<a href="(.+?)">\s+<span class="title">(.+?)</span>').findall(r)
            url = [i for i in r if title in i[1] and year in i[1]][0][0]
            url = client.request(url, headers=self.headers)
            url = re.compile('<a href="(.+?)" target="_blank">\s+<span class="label">Source #.+?</span>').findall(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            if 'tvshowtitle' in data:
                url = self.searchShow(title, int(data['season']), int(data['episode']), data['year'])
            else:
                url = self.searchMovie(title, data['year'])
            for url in url:
                valid, hoster = source_utils.is_host_valid(url, hostDict)
                if valid:
                    sources.append({'source': hoster, 'quality': 'HD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---ICEFILMS Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url

