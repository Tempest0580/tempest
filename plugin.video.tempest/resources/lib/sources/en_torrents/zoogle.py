# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 02-24-2019 by JewBMX in Scrubs.

import re,urllib,urlparse
import traceback
from resources.lib.modules import log_utils
from resources.lib.modules import cleantitle,client,control,debrid,source_utils,workers
from resources.lib.modules import rd_check, control


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['zooqle.com']
        self.base_link = 'https://zooqle.com'
        self.search_link = '/search?q=%s'
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
        try:
            sources = []
            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            category = '+category%3ATV' if 'tvshowtitle' in data else '+category%3AMovies'
            query = '%s S%02dE%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|<|>|\|)', ' ', query)
            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url) + str(category)
            html = client.request(url, headers=self.headers)
            html = html.replace('&nbsp;', ' ')
            try:
                results = client.parseDOM(html, 'table', attrs={'class': 'table table-condensed table-torrents vmiddle'})[0]
            except:
                return sources
            rows = re.findall('<tr(.+?)</tr>', results, re.DOTALL)
            if rows is None:
                return sources
            for entry in rows:
                try:
                    try:
                        name = re.findall('<a class=".+?>(.+?)</a>', entry, re.DOTALL)[0]
                        name = client.replaceHTMLCodes(name).replace('<hl>', '').replace('</hl>', '')
                        if not cleantitle.get(title) in cleantitle.get(name):
                            continue
                    except:
                        continue
                    y = re.findall('[\.|\(|\[|\s](\d{4}|S\d*E\d*|S\d*)[\.|\)|\]|\s]', name)[-1].upper()
                    if not y == hdlr:
                        continue
                    try:
                        seeders = int(re.findall('class="progress prog trans90" title="Seeders: (.+?) \|', entry, re.DOTALL)[0])
                    except:
                        continue
                    if self.min_seeders > seeders:
                        continue
                    try:
                        link = 'magnet:%s' % (re.findall('href="magnet:(.+?)"', entry, re.DOTALL)[0])
                        link = str(client.replaceHTMLCodes(link).split('&tr')[0])
                    except:
                        continue
                    quality, info = source_utils.get_release_quality(name, name)
                    try:
                        size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|MB|MiB))', entry)[-1]
                        div = 1 if size.endswith(('GB', 'GiB')) else 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size)) / div
                        size = '%.2f GB' % size
                        info.append(size)
                    except:
                        pass
                    info = ' | '.join(info)
                    if control.setting('torrent.rd_check') == 'true':
                        checked = rd_check.rd_cache_check(url)
                        if checked:
                            sources.append(
                                {'source': 'Cached Torrent', 'quality': quality, 'language': 'en', 'url': checked,
                                 'info': info, 'direct': False, 'debridonly': True})
                    else:
                        sources.append(
                            {'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': link,
                             'info': info, 'direct': False, 'debridonly': True})
                except:
                    continue
            check = [i for i in sources if not i['quality'] == 'CAM']
            if check:
                sources = check
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---Zoogle Testing - Exception: \n' + str(failure))
            return self._sources

    def resolve(self, url):
        return url
