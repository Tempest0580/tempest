# -*- coding: utf-8 -*-
# -Rewrote on 06-14-2020 by Tempest.

import re, urllib, urlparse
import traceback
from resources.lib.modules import client,  log_utils
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['projecfreetv.co']
        self.base_link = 'https://projecfreetv.co'
        self.search_link = '/episode/%s/'
        self.headers = {'User-Agent': client.agent()}

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
        try:
            sources = []

            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            hdlr = 's%02de%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s-s%02de%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode']))
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url).replace('+', '-')

            r = client.request(url, headers=self.headers)
            try:
                data = re.compile('<a href="(.+?)" target="_blank" rel="nofollow" title.+?').findall(r)
                for url in data:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        sources.append(
                            {'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False,
                             'debridonly': False})
            except:
                pass
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---PROJECTFREETV Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
