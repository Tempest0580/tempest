# -*- coding: utf-8 -*-
"""
    **Created by Tempest**
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""

import re, urllib, urlparse
from resources.lib.modules import cleantitle, debrid, source_utils
from resources.lib.modules import client, rd_check, control


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['torrentgalaxy.to']
        self.base_link = 'https://torrentgalaxy.to/'
        self.search_link = 'torrents.php?search=%s'
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

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None:
                return sources
            if debrid.status() is False:
                raise Exception()
            if debrid.torrent_enabled() is False:
                raise Exception()
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
                posts = re.findall('a href="(magnet:.+?)"', r, re.DOTALL)
                for post in posts:
                    try:
                        size = re.findall("style='border-radius:4px;'>(.+?)</span>", r, re.DOTALL)
                        size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', size)[0]
                        div = 1 if size.endswith('GB') else 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size.replace(',', '.'))) / div
                        size = '%.2f GB' % size
                    except BaseException:
                        size = '0'
                    url = post.split('&tr')[0]
                    if hdlr not in url:
                        continue
                    quality, info = source_utils.get_release_quality(url)
                    if any(x in url for x in ['FRENCH', 'Ita', 'italian', 'TRUEFRENCH', '-lat-', 'Dublado']):
                        continue
                    info.append(size)
                    info = ' | '.join(info)
                    if control.setting('torrent.rd_check') == 'true':
                        checked = rd_check.rd_cache_check(url)
                        if checked:
                            sources.append(
                                {'source': 'Cached Torrent', 'quality': quality, 'language': 'en', 'url': checked,
                                 'info': ' | '.join(info), 'direct': False, 'debridonly': True})
                    else:
                        sources.append(
                            {'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url,
                             'info': info, 'direct': False, 'debridonly': True})
            except:
                return
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
