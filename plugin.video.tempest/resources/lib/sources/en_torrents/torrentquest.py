# -*- coding: utf-8 -*-
# -Cleaned and Checked on 06-17-2019 by JewBMX in Scrubs.

import re,urllib,urlparse
import traceback
from resources.lib.modules import client,cleantitle,debrid,source_utils
from resources.lib.modules import log_utils
from resources.lib.modules import rd_check, control


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en', 'de', 'fr', 'ko', 'pl', 'pt', 'ru']
        self.domains = ['torrentquest.com']
        self.base_link = 'https://torrentquest.com'
        self.search_link = '/{0}/{1}'
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
            if url == None:
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
            query = '%s s%02de%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode']))\
                if 'tvshowtitle' in data else '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            url = urlparse.urljoin(self.base_link, self.search_link.format(query[0].lower(), cleantitle.geturl(query)))
            r = client.request(url, headers=self.headers)
            r = client.parseDOM(r, 'tbody')[0]
            posts = client.parseDOM(r, 'tr')
            posts = [i for i in posts if 'magnet:' in i]
            for post in posts:
                post = post.replace('&nbsp;', ' ')
                name = client.parseDOM(post, 'a', ret='title')[1]
                t = name.split(hdlr)[0]
                if not cleantitle.get(re.sub('(|)', '', t)) == cleantitle.get(title):
                    continue
                try:
                    y = re.findall('[\.|\(|\[|\s|\_|\-](S\d+E\d+|S\d+)[\.|\)|\]|\s|\_|\-]', name, re.I)[-1].upper()
                except:
                    y = re.findall('[\.|\(|\[|\s\_|\-](\d{4})[\.|\)|\]|\s\_|\-]', name, re.I)[-1].upper()
                if not y == hdlr:
                    continue
                links = client.parseDOM(post, 'a', ret='href')
                magnet = [i.replace('&amp;', '&') for i in links if 'magnet:' in i][0]
                url = magnet.split('&tr')[0]
                if url in str(sources):
                    continue
                quality, info = source_utils.get_release_quality(name, name)
                try:
                    size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', post)[0]
                    div = 1 if size.endswith(('GB', 'GiB')) else 1024
                    size = float(re.sub('[^0-9|/.|/,]', '', size.replace(',', '.'))) / div
                    size = '%.2f GB' % size
                except:
                    size = '0'
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
                        {'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                         'direct': False, 'debridonly': True})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---TorrentQuest Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
