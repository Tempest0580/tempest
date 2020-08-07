# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re, base64
import traceback
from resources.lib.modules import client,  log_utils
from resources.lib.modules import source_utils
from resources.lib.modules import tvmaze


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.genre_filter = ['animation', 'anime']
        self.domains = ['animeram.cc']
        self.base_link = 'https://ww2.animeram.cc'
        self.show_link = '/%s/%s'
        self.tv_maze = tvmaze.tvMaze()
        self.headers = {'User-Agent': client.agent()}

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            tvshowtitle = self.tv_maze.showLookup('thetvdb', tvdb)
            url = tvshowtitle['name']
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            num = self.tv_maze.episodeAbsoluteNumber(tvdb, int(season), int(episode))
            url = self.base_link + self.show_link % (url.lower(), num)
            url = url.replace(' ', '-')
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            page = client.request(url, headers=self.headers)
            links = re.compile('<iframe src="(.+?)"', re.DOTALL).findall(page)
            for link in links:
                if '/recaptcha/' in link:
                    continue
                link = "https:" + link if not link.startswith('http') else link
                page2 = client.request(link)
                urls = re.compile('label: "(.+?)", bk: "(.+?)"', re.DOTALL).findall(page2)
                for qual, url in urls:
                    url = base64.b64decode(url)
                    url = client.replaceHTMLCodes(url.replace('%3A', ':').replace('%2F', '/'))
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        quality, info = source_utils.get_release_quality(qual, url)
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': True, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---ANIMERAM Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
