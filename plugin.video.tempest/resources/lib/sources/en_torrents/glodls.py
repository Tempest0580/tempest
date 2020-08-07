# -*- coding: utf-8 -*-
# -Cleaned and Checked on 03-04-2019 by JewBMX in Scrubs.

import re,urllib,urlparse
import traceback
from resources.lib.modules import client2 as client
from resources.lib.modules import cleantitle2 as cleantitle
from resources.lib.modules import debrid,source_utils,control
from resources.lib.modules import log_utils
from resources.lib.modules import rd_check, control


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['glodls.to']
        self.base_link = 'https://glodls.to/'
        self.tvsearch = 'search_results.php?search={0}&cat=41&incldead=0&inclexternal=0&lang=1&sort=seeders&order=desc'
        self.moviesearch = 'search_results.php?search={0}&cat=1&incldead=0&inclexternal=0&lang=1&sort=size&order=desc'
        self.min_seeders = int(control.setting('torrent.min.seeders'))
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
        sources = []
        try:
            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            self.title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            query = '%s S%02dE%02d' % (
            data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (
            data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            if 'tvshowtitle' in data:
                url = self.tvsearch.format(urllib.quote_plus(query))
                url = urlparse.urljoin(self.base_link, url)
            else:
                url = self.moviesearch.format(urllib.quote_plus(query))
                url = urlparse.urljoin(self.base_link, url)
            items = self._get_items(url)
            for item in items:
                try:
                    name = item[0]
                    quality, info = source_utils.get_release_quality(name, name)
                    info.append(item[2])
                    url = item[1]
                    url = url.split('&tr')[0]
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
                except BaseException:
                    pass
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---Glodls Testing - Exception: \n' + str(failure))
            return sources

    def _get_items(self, url):
        items = []
        try:
            r = client.request(url, headers=self.headers)
            posts = client.parseDOM(r, 'tr', attrs={'class': 't-row'})
            posts = [i for i in posts if not 'racker:' in i]
            for post in posts:
                data = client.parseDOM(post, 'a', ret='href')
                url = [i for i in data if 'magnet:' in i][0]
                seeders = re.findall(
                    "<td class='ttable_col2' align='center'><font color='green'><b>(.+?)</b></font></td>", post)[0]
                if self.min_seeders > seeders:
                    continue
                name = client.parseDOM(post, 'a', ret='title')[0]
                t = name.split(self.hdlr)[0]
                if not cleantitle.get(re.sub('(|)', '', t)) == cleantitle.get(self.title): continue
                try:
                    y = re.findall('[\.|\(|\[|\s|\_|\-](S\d+E\d+|S\d+)[\.|\)|\]|\s|\_|\-]', name, re.I)[-1].upper()
                except BaseException:
                    y = re.findall('[\.|\(|\[|\s\_|\-](\d{4})[\.|\)|\]|\s\_|\-]', name, re.I)[-1].upper()
                if not y == self.hdlr: continue
                try:
                    size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', post)[0]
                    div = 1 if size.endswith('GB') else 1024
                    size = float(re.sub('[^0-9|/.|/,]', '', size.replace(',', '.'))) / div
                    size = '%.2f GB' % size
                except BaseException:
                    size = '0'
                items.append((name, url, size))
            return items
        except BaseException:
            return items

    def resolve(self, url):
        return url
