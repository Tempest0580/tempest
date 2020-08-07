# -*- coding: UTF-8 -*-
# -Created from the one by JewBMX in Scrubs.
# -Update by Tempest (Pulls links for RD users)

import re, urllib, urlparse
import traceback
from resources.lib.sources import cfscrape
from resources.lib.modules import log_utils
from resources.lib.modules import cleantitle, client
from resources.lib.modules import source_utils, rd_check
from resources.lib.modules import debrid, control


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['soapgate.online', 'fmovies.tw', 'ganool.ws', 'ganol.si', 'ganool123.com']
        self.base_link = 'https://idtube.ru'
        self.search_link = '/search/?q=%s'
        self.headers = {'User-Agent': client.agent()}

    def movie(self, imdb, title, localtitle, aliases, year):
        if debrid.status() is False: return
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            q = '%s' % cleantitle.get_gan_url(data['title'])
            url = urlparse.urljoin(self.base_link, self.search_link % q)
            r = cfscrape.get(url, headers=self.headers).content
            v = re.compile('<a href="(.+?)" class="ml-mask jt" title="(.+?)">\s+<span class=".+?">(.+?)</span>').findall(r)
            for url, check, quality in v:
                t = '%s (%s)' % (data['title'], data['year'])
                if t in check:
                    key = url.split('-hd')[1]
                    url = 'https://ganool1.com//moviedownload.php?q=%s' % key
                    r = cfscrape.get(url, headers=self.headers).content
                    r = re.compile('<a rel=".+?" href="(.+?)" target=".+?">').findall(r)
                    for url in r:
                        if any(x in url for x in ['.rar']): continue
                        quality, info = source_utils.get_release_quality(quality, url)
                        valid, host = source_utils.is_host_valid(url, hostDict)
                        if valid:
                            info = ' | '.join(info)
                            if control.setting('deb.rd_check') == 'true':
                                check = rd_check.rd_deb_check(url)
                                if check:
                                    info = 'RD Checked' + ' | ' + info
                                    sources.append(
                                        {'source': host, 'quality': quality, 'language': 'en', 'url': check,
                                         'info': info, 'direct': False, 'debridonly': True})
                            else:
                                sources.append(
                                    {'source': host, 'quality': quality, 'language': 'en', 'url': url,
                                     'info': info, 'direct': False, 'debridonly': True})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---Ganool Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
