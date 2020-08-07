# -*- coding: utf-8 -*-

"""
    **Created by Tempest**
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""


import re, urllib, urlparse, json, traceback
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils
from resources.lib.modules import log_utils
from resources.lib.modules import rd_check
from resources.lib.modules import debrid


class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['https://solidtorrents.net']
        self.base_link = 'https://solidtorrents.net'
        self.search_link = '/api/v1/search?q=%s&category=all&sort=size'
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
            if url is None: return

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

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            imdb_id = data['imdb']

            query = '%s S%02dE%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(query))

            r = client.request(url, headers=self.headers)

            result = json.loads(r)
            result = result['results']

            items = []

            for item in result:
                try:
                    name = item['title']
                    url = item['magnet']

                    size = ''
                    try:
                        size = item['size']
                        size = float(size)/(1024**3)
                        size = '%.2f GB' % size
                    except:
                        pass

                    t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d+|3D)(\.|\)|\]|\s|)(.+|)', '', name)
                    if not cleantitle.get(t) == cleantitle.get(title): raise Exception()
                    y = re.findall('[\.|\(|\[|\s](\d{4}|(?:S|s)\d*(?:E|e)\d*|(?:S|s)\d*)[\.|\)|\]|\s]', name)[-1].upper()
                    if not y == hdlr: raise Exception()

                    quality, info = source_utils.get_release_quality(name, name)
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
                             'info': ' | '.join(info), 'direct': False, 'debridonly': True})
                    
                except:
                    pass

            return sources
        except:
            failure = traceback.format_exc()
            log_utils.log('---SolidTorrents Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
