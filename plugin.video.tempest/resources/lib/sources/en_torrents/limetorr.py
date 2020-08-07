# -*- coding: utf-8 -*-
# -Cleaned and Checked on 03-04-2019 by JewBMX in Scrubs.

import re,urllib,urlparse
import traceback
from resources.lib.modules import client2 as client
from resources.lib.modules import dom_parser2 as dom
from resources.lib.modules import cleantitle2 as cleantitle
from resources.lib.modules import debrid,source_utils,workers,control
from resources.lib.modules import log_utils
from resources.lib.modules import rd_check, control


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['limetorrents.info']
        self.base_link = 'https://www.limetorrents.info'
        self.tvsearch = 'https://www.limetorrents.info/search/tv/{0}/'
        self.moviesearch = 'https://www.limetorrents.info/search/movies/{0}/'
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
            self._sources = []
            self.items = []
            if url is None:
                return self._sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            self.title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            query = '%s S%02dE%02d' % (
            data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (
            data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            if 'tvshowtitle' in data:
                url = self.tvsearch.format(urllib.quote(query))
            else:
                url = self.moviesearch.format(urllib.quote(query))
            self._get_items(url)
            self.hostDict = hostDict + hostprDict
            threads = []
            for i in self.items:
                threads.append(workers.Thread(self._get_sources, i))
            [i.start() for i in threads]
            [i.join() for i in threads]
            return self._sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---Limetorr Testing - Exception: \n' + str(failure))
            return self._sources

    def _get_items(self, url):
        try:
            r = client.request(url, headers=self.headers)
            posts = client.parseDOM(r, 'table', attrs={'class': 'table2'})[0]
            posts = client.parseDOM(posts, 'tr')
            for post in posts:
                data = dom.parse_dom(post, 'a', req='href')[1]
                link = urlparse.urljoin(self.base_link, data.attrs['href'].replace('- -', '+').replace(' ', '+').replace('-\xe2\xad\x90-', '+'))
                name = data.content
                t = name.split(self.hdlr)[0]
                if not cleantitle.get(re.sub('(|)', '', t)) == cleantitle.get(self.title):
                    continue
                try:
                    y = re.findall('[\.|\(|\[|\s|\_|\-](S\d+E\d+|S\d+)[\.|\)|\]|\s|\_|\-]', name, re.I)[-1].upper()
                except:
                    y = re.findall('[\.|\(|\[|\s\_|\-](\d{4})[\.|\)|\]|\s\_|\-]', name, re.I)[-1].upper()
                if not y == self.hdlr: continue
                try:
                    size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', post)[0]
                    div = 1 if size.endswith('GB') else 1024
                    size = float(re.sub('[^0-9|/.|/,]', '', size.replace(',', '.'))) / div
                    size = '%.2f GB' % size
                except BaseException:
                    size = '0'
                self.items.append((name, link, size))
            return self.items
        except:
            return self.items

    def _get_sources(self, item):
        try:
            name = item[0]
            quality, info = source_utils.get_release_quality(name, name)
            info.append(item[2])
            data = client.request(item[1], headers=self.headers)
            url = re.search('''href=["'](magnet:\?[^"']+)''', data).groups()[0]
            url = url.split('&tr')[0]
            info = ' | '.join(info)
            if control.setting('torrent.rd_check') == 'true':
                checked = rd_check.rd_cache_check(url)
                if checked:
                    self._sources.append(
                        {'source': 'Cached Torrent', 'quality': quality, 'language': 'en', 'url': checked,
                         'info': ' | '.join(info), 'direct': False, 'debridonly': True})
            else:
                self._sources.append(
                    {'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                     'direct': False, 'debridonly': True})
        except:
            pass

    def resolve(self, url):
        return url
