# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 08-24-2019 by JewBMX in Scrubs.
# Was xpause fix by Tempest on 10-13-2019

import re, urllib, urlparse
import traceback
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import debrid
from resources.lib.modules import source_utils
from resources.lib.modules import log_utils
from resources.lib.modules import rd_check, control


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['topnow.se']
        self.base_link = 'http://topnow.se'
        self.search_link = '/index.php?search=%s'
        self.search_show = '/index.php?show=%s'
        self.headers = {'User-Agent': client.agent()}

    def movie(self, imdb, title, localtitle, aliases, year):
        if debrid.status() is False: return
        if debrid.torrent_enabled() is False: return
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        if debrid.status() is False: return
        if debrid.torrent_enabled() is False: return
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        if debrid.status() is False: return
        if debrid.torrent_enabled() is False: return
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

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s (%s)' % (data['title'].replace(' (and the Fantabulous Emancipation of One Harley Quinn)',''), data['year'])

            query = '%s' % data['tvshowtitle'].replace(' ', '+') if 'tvshowtitle' in data else '%s' % (data['title'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            if 'tvshowtitle' in data:
                url = self.search_show % query.replace('+','-')
            else:
                url = self.search_link % query.replace('  ', '+').replace(' ', '+')
            url = urlparse.urljoin(self.base_link, url)

            html = client.request(url, headers=self.headers)
            html = client.parseDOM(html, 'div', attrs={'class': 'card'})
            for r in html:
                name = re.findall('src=".+?" alt="(.+?)"', r, re.DOTALL)[0]
                name = name.replace(u'\xa0', ' ')
                if hdlr in name:
                    link = re.findall('href="(magnet:.+?)"', r, re.DOTALL)[0]
                    link = client.replaceHTMLCodes(link).split('&tr')[0]
                    quality, info = source_utils.get_release_quality(link, link)
                    try:
                        size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|MB|MiB))', html)[-1]
                        div = 1 if size.endswith(('GB', 'GiB')) else 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size)) / div
                        size = '%.2f GB' % size
                        info.append(size)
                    except:
                        pass
                    info = ' | '.join(info)
                    if control.setting('torrent.rd_check') == 'true':
                        checked = rd_check.rd_cache_check(link)
                        if checked:
                            sources.append(
                                {'source': 'Cached Torrent', 'quality': quality, 'language': 'en','url': checked,
                                 'info': info, 'direct': False, 'debridonly': True})
                    else:
                        sources.append(
                            {'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': link, 'info': info,
                             'direct': False, 'debridonly': True})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---Topnow Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
