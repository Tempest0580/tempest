# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.
# -Cleaned and Checked on 04-30-2020 by Tempest.

import traceback
from resources.lib.modules import cleantitle, log_utils
from resources.lib.modules import directstream
from resources.lib.modules import getSum
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']  # watchserieshd.co got changed to a different source
        self.domains = ['watchserieshd.tv', 'watchserieshd.cc']  # Old  watchserieshd.io
        self.base_link = 'https://www3.watchserieshd.tv'
        self.search_link = '/series/%s-season-%s-episode-%s'

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
            url = self.base_link + self.search_link % (url, season, episode)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None:
                return sources
            hostDict = hostprDict + hostDict
            r = getSum.get(url)
            match = getSum.findSum(r)
            for url in match:
                if 'load.php' not in url:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        quality, info = source_utils.get_release_quality(url, url)
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---WATCHSERIESHD Testing - Exception: \n' + str(failure))
            return sources


def resolve(self, url):
        if "google" in url:
            return directstream.googlepass(url)
        else:
            return url
