# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 02-24-2019 by JewBMX in Scrubs.

import re,urllib,urlparse
import traceback
from resources.lib.modules import log_utils
from resources.lib.modules import cleantitle,client,control,debrid,source_utils
from resources.lib.modules import rd_check, control


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['yts.am']
        self.base_link = 'https://yts.mx/'
        self.search_link = 'browse-movies/%s/all/all/0/latest'
        self.min_seeders = int(control.setting('torrent.min.seeders'))
        self.headers = {'User-Agent': client.agent()}

    def movie(self, imdb, title, localtitle, aliases, year):
        if debrid.status() is False: return
        if debrid.torrent_enabled() is False: return
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            query = '%s %s' % (data['title'], data['year'])
            url = self.search_link % urllib.quote(query)
            url = urlparse.urljoin(self.base_link, url)
            html = client.request(url, headers=self.headers)
            try:
                results = client.parseDOM(html, 'div', attrs={'class': 'row'})[2]
            except:
                return sources
            items = re.findall('class="browse-movie-bottom">(.+?)</div>\s</div>', results, re.DOTALL)
            if items is None:
                return sources
            for entry in items:
                try:
                    try:
                        link, name = re.findall('<a href="(.+?)" class="browse-movie-title">(.+?)</a>', entry, re.DOTALL)[0]
                        name = client.replaceHTMLCodes(name)
                        if not cleantitle.get(name) == cleantitle.get(data['title']):
                            continue
                    except:
                        continue
                    y = entry[-4:]
                    if not y == data['year']:
                        continue
                    response = client.request(link, headers=self.headers)
                    try:
                        entries = client.parseDOM(response, 'div', attrs={'class': 'modal-torrent'})
                        for torrent in entries:
                            link, name = re.findall('href="magnet:(.+?)" class="magnet-download download-torrent magnet" title="(.+?)"', torrent, re.DOTALL)[0]
                            link = 'magnet:%s' % link
                            link = str(client.replaceHTMLCodes(link).split('&tr')[0])
                            quality, info = source_utils.get_release_quality(name, name)
                            try:
                                size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|MB|MiB))', torrent)[-1]
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
                                        {'source': 'Cached Torrent', 'quality': quality, 'language': 'en',
                                         'url': checked, 'info': info, 'direct': False, 'debridonly': True})
                            else:
                                sources.append(
                                    {'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': link,
                                     'info': info, 'direct': False, 'debridonly': True})
                    except:
                        continue
                except:
                    continue
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---Ytsam Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
