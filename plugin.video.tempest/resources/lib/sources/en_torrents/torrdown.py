# -*- coding: utf-8 -*-
# -Cleaned and Checked on 03-04-2019 by JewBMX in Scrubs.

import re,urllib,urlparse
import traceback
from resources.lib.modules import client2 as client
from resources.lib.modules import cleantitle2 as cleantitle
from resources.lib.modules import debrid,source_utils,workers,control
from resources.lib.modules import log_utils
from resources.lib.modules import rd_check, control


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['limetorrents.info', 'torrentdownloads.me']
        self.base_link = 'https://www.torrentdownloads.me'
        self.search = 'https://www.torrentdownloads.me/rss.xml?new=1&type=search&cid={0}&search={1}'
        self.headers = {'User-Agent': client.agent()}

    def movie(self, imdb, title, localtitle, aliases, year):
        if debrid.status() is False: return
        if debrid.torrent_enabled() is False: return
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except BaseException:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        if debrid.status() is False: return
        if debrid.torrent_enabled() is False: return
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except BaseException:
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
        except BaseException:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            self._sources = []
            if url is None:
                return self._sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            self.title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            query = '%s S%02dE%02d' % (
            data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (
            data['title'], data['year'])
            query = re.sub(r'(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            if 'tvshowtitle' in data:
                url = self.search.format('8', urllib.quote(query))
            else:
                url = self.search.format('4', urllib.quote(query))
            self.hostDict = hostDict + hostprDict
            _html = client.request(url, headers=self.headers)
            threads = []
            for i in re.findall(r'<item>(.+?)</item>', _html, re.DOTALL):
                threads.append(workers.Thread(self._get_items, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            return self._sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---Torrdown Testing - Exception: \n' + str(failure))
            return self._sources

    def _get_items(self, r):
        try:
            size = re.search(r'<size>([\d]+)</size>', r).groups()[0]
            seeders = re.search(r'<seeders>([\d]+)</seeders>', r).groups()[0]
            _hash = re.search(r'<info_hash>([a-zA-Z0-9]+)</info_hash>', r).groups()[0]
            name = re.search(r'<title>(.+?)</title>', r).groups()[0]
            url = 'magnet:?xt=urn:btih:%s&dn=%s' % (_hash.upper(), urllib.quote_plus(name))
            url = url.split('&tr')[0]
            t = name.split(self.hdlr)[0]
            try:
                y = re.findall(r'[\.|\(|\[|\s|\_|\-](S\d+E\d+|S\d+)[\.|\)|\]|\s|\_|\-]', name, re.I)[-1].upper()
            except:
                y = re.findall(r'[\.|\(|\[|\s\_|\-](\d{4})[\.|\)|\]|\s\_|\-]', name, re.I)[-1].upper()
            try:
                div = 1000 ** 3
                size = float(size) / div
                size = '%.2f GB' % size
            except:
                size = '0'
            quality, info = source_utils.get_release_quality(name, name)
            info.append(size)
            info = ' | '.join(info)
            if not seeders == '0':
                if cleantitle.get(re.sub('(|)', '', t)) == cleantitle.get(self.title):
                    if y == self.hdlr:
                        if control.setting('torrent.rd_check') == 'true':
                            checked = rd_check.rd_cache_check(url)
                            if checked:
                                self._sources.append(
                                    {'source': 'Cached Torrent', 'quality': quality, 'language': 'en',  'url': checked,
                                     'info': info, 'direct': False, 'debridonly': True})
                        else:
                            self._sources.append(
                                {'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url,
                                 'info': info, 'direct': False, 'debridonly': True})
        except:
            pass

    def resolve(self, url):
        return url
