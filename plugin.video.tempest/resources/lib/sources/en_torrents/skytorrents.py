# -*- coding: utf-8 -*-
"""
    **Created by Tempest**
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""

import re, urllib, urlparse
import traceback
from resources.lib.modules import cleantitle, debrid, source_utils
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import log_utils
from resources.lib.modules import rd_check


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['www.skytorrents.lol']
        self.base_link = 'https://www.skytorrents.lol/'
        self.search_link = '?query=%s'
        self.min_seeders = int(control.setting('torrent.min.seeders'))
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
        sources = []
        try:
            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s s%02de%02d' % (
            data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (
            data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)

            try:
                r = client.request(url, headers=self.headers)
                posts = client.parseDOM(r, 'tbody')[0]
                posts = client.parseDOM(posts, 'tr')
                for post in posts:
                    link = re.findall('a href="(magnet:.+?)" title="(.+?)"', post, re.DOTALL)
                    try:
                        size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', post)[0]
                        div = 1 if size.endswith('GB') else 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size.replace(',', '.'))) / div
                        size = '%.2f GB' % size
                    except BaseException:
                        size = '0'
                    for url, data in link:
                        if hdlr not in data:
                            continue
                        url = url.split('&tr')[0]
                        quality, info = source_utils.get_release_quality(data)
                        if any(x in url for x in ['FRENCH', 'Ita', 'ITA', 'italian', 'Tamil', 'TRUEFRENCH', '-lat-', 'Dublado', 'Dub', 'Rus', 'Hindi']):
                            continue
                        info.append(size)
                        info = ' | '.join(info)
                        if control.setting('torrent.rd_check') == 'true':
                            checked = rd_check.rd_cache_check(url)
                            if checked:
                                sources.append(
                                    {'source': 'Cached Torrent', 'quality': quality, 'language': 'en', 'url': checked,
                                     'info': info, 'direct': False, 'debridonly': True})
                        else:
                            sources.append(
                                {'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url,
                                 'info': info, 'direct': False, 'debridonly': True})
            except:
                return
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---Skytorrents Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
