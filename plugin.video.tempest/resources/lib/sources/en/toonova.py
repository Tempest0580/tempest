# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.
# -Cleaned and Checked on 04-14-2020 by Tempest.

import re
import traceback
from resources.lib.modules import client, log_utils
from resources.lib.modules import cleantitle
from resources.lib.modules import source_tools


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.genre_filter = ['animation', 'anime']
        self.domains = ['toonova.net']
        self.base_link = 'http://toonova.net'
        self.headers = {'User-Agent': client.agent()}

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = '%s-%s' % (title, year)
            url = self.base_link + '/' + url
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            if season == '1': 
                url = self.base_link + '/' + url + '-episode-' + episode
            else:
                url = self.base_link + '/' + url + '-season-' + season + '-episode-' + episode
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            r = client.request(url, headers=self.headers)
            match = re.compile('<iframe src="(.+?)"').findall(r)
            for url in match:
                r = client.request(url, headers=self.headers)
                if 'playpanda' in url:
                    match = re.compile("url: '(.+?)',").findall(r)
                else:
                    match = re.compile('file: "(.+?)",').findall(r)
                for url in match:
                    url = url.replace('\\', '')
                    if url in str(sources):
                        continue
                    info = source_tools.get_info(url)
                    quality = source_tools.get_quality(url)
                    sources.append({'source': 'Direct', 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---TOONOVA Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
