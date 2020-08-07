# -*- coding: utf-8 -*-
"""
    **Sent to me by email**
"""

import re
import urllib
import urlparse
import traceback
from resources.lib.modules import log_utils
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser
from resources.lib.modules import workers, debrid
from resources.lib.modules import rd_check, control


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['www.mkvhub.net', 'www.mkvhub.com']
        self.base_link = 'https://www.mkvhub.net'
        self.search_link = '/?s=%s'
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
            self._sources = []

            if url is None:
                return self._sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s S%02dE%02d' % (data['tvshowtitle'], int(data['season']),  int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url, headers=self.headers)

            posts = client.parseDOM(r, 'figure')

            items = []
            for post in posts:
                try:
                    tit = client.parseDOM(post, 'img', ret='title')[0]

                    t = tit.split(hdlr)[0].replace('(', '')
                    if not cleantitle.get(t) == cleantitle.get(title):
                        raise Exception()

                    if hdlr not in tit:
                        raise Exception()

                    url = client.parseDOM(post, 'a', ret='href')[0]

                    try:
                        size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', post)[0]
                        div = 1 if size.endswith(('GB', 'GiB', 'Gb')) else 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size.replace(',', '.'))) / div
                        size = '%.2f GB' % size
                    except:
                        size = '0'

                    items += [(tit, url, size)]

                except:
                    pass

            datos = []
            for title, url, size in items:
                try:
                    name = client.replaceHTMLCodes(title)

                    quality, info = source_utils.get_release_quality(name, name)

                    info.append(size)
                    info = ' | '.join(info)

                    datos.append((url, quality, info))
                except:
                    pass

            threads = []
            for i in datos:
                threads.append(workers.Thread(self._get_sources, i[0], i[1], i[2], hostDict, hostprDict))
            [i.start() for i in threads]
            [i.join() for i in threads]

            return self._sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---Mkvhub Testing - Exception: \n' + str(failure))
            return self._sources

    def _get_sources(self, url, quality, info, hostDict, hostprDict):
        urls = []

        result = client.request(url, headers=self.headers)

        urls = [(client.parseDOM(result, 'a', ret='href', attrs={'class': 'dbuttn watch'})[0],
                client.parseDOM(result, 'a', ret='href', attrs={'class': 'dbuttn blue'})[0],
                client.parseDOM(result, 'a', ret='href', attrs={'class': 'dbuttn magnet'})[0])]

        for url in urls[0]:
            try:
                r = client.request(url, headers={'User-Agent': client.agent()})

                if 'linkomark' in url:
                    p_link = dom_parser.parse_dom(r, 'link', {'rel': 'canonical'},  req='href')[0]
                    p_link = p_link.attrs['href']
                    input_name = client.parseDOM(r, 'input', ret='name')[0]
                    input_value = client.parseDOM(r, 'input', ret='value')[0]
                    post = {input_name: input_value}
                    p_data = client.request(p_link, post=post, headers=self.headers)
                    links = client.parseDOM(p_data, 'a', ret='href', attrs={'target': '_blank'})

                    for i in links:
                        valid, host = source_utils.is_host_valid(i, hostDict)
                        if not valid:
                            valid, host = source_utils.is_host_valid(i, hostprDict)
                            if not valid:
                                continue
                            else:
                                rd = True
                        else:
                            rd = False
                        if i in str(self._sources):
                            continue

                        if 'rapidgator' in i:
                            rd = True

                        if rd:
                            if debrid.status() is False: return
                            if control.setting('deb.rd_check') == 'true':
                                checked = rd_check.rd_deb_check(url)
                                if checked:
                                    info = 'RD Checked' + ' | ' + info
                                    self._sources.append(
                                        {'source': host, 'quality': quality, 'language': 'en', 'url': checked,
                                         'info': info, 'direct': False, 'debridonly': True})
                            else:
                                self._sources.append(
                                    {'source': host, 'quality': quality, 'language': 'en', 'url': i,
                                     'info': info, 'direct': False, 'debridonly': True})
                        else:
                            self._sources.append(
                                {'source': host, 'quality': quality, 'language': 'en', 'url': i,
                                 'info': info, 'direct': False, 'debridonly': False})

                elif 'torrent' in url:
                    if debrid.torrent_enabled() is False: return self._sources
                    data = client.parseDOM(r, 'a', ret='href')
                    url = [i for i in data if 'magnet:' in i][0]
                    url = url.split(';tr')[0]
                    if control.setting('torrent.rd_check') == 'true':
                        checked = rd_check.rd_cache_check(url)
                        if checked:
                            self._sources.append(
                                {'source': 'Cahced Torrent', 'quality': quality, 'language': 'en', 'url': checked,
                                 'info': info,  'direct': False, 'debridonly': True})
                    else:
                        self._sources.append(
                            {'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url,
                             'info': info, 'direct': False, 'debridonly': True})

            except:
                pass

    def resolve(self, url):
        return url
