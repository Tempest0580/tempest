# Needs testing
# -*- coding: utf-8 -*-

"""
    **Created by Tempest**
    **If you see this in a addon other than Tempest and says it was
    created by someone other than Tempest they stole it from me**
"""


import re,urllib,urlparse
import traceback
from resources.lib.modules import client,  log_utils
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['divxcrawler.media']
        self.base_link = 'https://moviedownload.video'
        self.search_link = '/latest.htm'
        self.search_link2 = '/streaming.htm'
        self.search_link3 = '/movies.htm'
        self.headers = {'User-Agent': client.agent()}

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            imdb = data['imdb']

            try:
                query = urlparse.urljoin(self.base_link, self.search_link)
                result = client.request(query, headers=self.headers)
                m = re.findall('<strong>Movie Size:</strong> (.+?)</span></td>\s*<.+?href="(.+?)".+?href="(.+?)"\s*onMouse', result, re.DOTALL)
                m = [(i[0], i[1], i[2]) for i in m if imdb in i[1]]
                if m:
                    link = m
                else:
                    query = urlparse.urljoin(self.base_link, self.search_link2)
                    result = client.request(query, headers=self.headers)
                    m = re.findall('<strong>Movie Size:</strong> (.+?)</span></td>\s*<.+?href="(.+?)".+?href="(.+?)"\s*onMouse', result, re.DOTALL)
                    m = [(i[0], i[1], i[2]) for i in m if imdb in i[1]]
                    if m:
                        link = m
                    else:
                        query = urlparse.urljoin(self.base_link, self.search_link3)
                        result = client.request(query, headers=self.headers)
                        m = re.findall('<strong>Movie Size:</strong> (.+?)</span></td>\s*<.+?href="(.+?)".+?href="(.+?)"\s*onMouse', result, re.DOTALL)
                        m = [(i[0], i[1], i[2]) for i in m if imdb in i[1]]
                        if m:
                            link = m

            except:
                return sources

            for item in link:
                try:

                    quality, info = source_utils.get_release_quality(item[2], None)

                    try:
                        size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|gb|GiB|MB|mb|MiB))', item[0])[-1]
                        log_utils(size)
                        div = 1 if size.endswith(('GB', 'gb', 'GiB')) else 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size)) / div
                        size = '%.2f GB' % size
                    except:
                        size = '0'
                    info.append(size)
                    info = ' | '.join(info)

                    url = item[2]
                    if any(x in url for x in ['.rar', '.zip', '.iso']): raise Exception()
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                                    'direct': True, 'debridonly': False})
                except:
                    pass

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---DIVXCRAWLER Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url


