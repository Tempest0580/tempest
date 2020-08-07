# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.
# -Cleaned up and Checked and Fixed on 4-30-2020 by Tempest.

import re, urllib, urlparse, base64, json, time
import traceback
from resources.lib.modules import client, log_utils
from resources.lib.modules import cleantitle
from resources.lib.modules import directstream
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['showbox.space']
        self.base_link = 'https://showbox.care'

# https://showbox.space/movie/porkys
# https://popcorntime.watch/movie/porkys
# https://putlockers.app/movie/porkys
# https://gomovies.trade/movie/porkys
# https://fmovies.press/movie/porkys
# https://gostream.mobi/movie/porkys

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
            if url is None:
                return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def searchShow(self, title, season, episode, headers):
        try:
            url = '%s/show/%s/season/%01d/episode/%01d' % (self.base_link, cleantitle.geturl(title), int(season), int(episode))
            url = client.request(url, headers=headers, output='geturl', timeout='10')
            return url
        except:
            return

    def searchMovie(self, title, year, headers):
        try:
            url = '%s/movie/%s' % (self.base_link, cleantitle.geturl(title))
            url = client.request(url, headers=headers, output='geturl', timeout='10')
            return url
        except:
            return

    def searchMovie2(self, title, year, headers):
        try:
            url = '%s/movie/%s-%s' % (self.base_link, cleantitle.geturl(title), year)
            url = client.request(url, headers=headers, output='geturl', timeout='10')
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
            imdb = data['imdb']
            headers = {}
            if 'tvshowtitle' in data:
                url = self.searchShow(title, int(data['season']), int(data['episode']), headers)
            else:
                url = self.searchMovie(title, data['year'], headers)
            r = client.request(url, headers=headers, output='extended', timeout='10')
            if imdb not in r[0]:
                url = self.searchMovie2(title, data['year'], headers)
                r = client.request(url, headers=headers, output='extended', timeout='10')
            cookie = r[4]; headers = r[3]; result = r[0]
            try:
                r = re.findall('(https:.*?redirector.*?)[\'\"]', result)
                for i in r:
                    sources.append({'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'language': 'en', 'url': i, 'direct': True, 'debridonly': False})
            except:
                pass
            try:
                auth = re.findall('__utmx=(.+)', cookie)[0].split(';')[0]
            except:
                auth = 'false'
            auth = 'Bearer %s' % urllib.unquote_plus(auth)
            headers['Authorization'] = auth
            headers['Referer'] = url
            u = '/ajax/vsozrflxcw.php'
            self.base_link = client.request(self.base_link, headers=headers, output='geturl')
            u = urlparse.urljoin(self.base_link, u)
            action = 'getEpisodeEmb' if '/episode/' in url else 'getMovieEmb'
            elid = urllib.quote(base64.encodestring(str(int(time.time()))).strip())
            token = re.findall("var\s+tok\s*=\s*'([^']+)", result)[0]
            idEl = re.findall('elid\s*=\s*"([^"]+)', result)[0]
            post = {'action': action, 'idEl': idEl, 'token': token, 'nopop': '', 'elid': elid}
            post = urllib.urlencode(post)
            cookie += ';%s=%s' % (idEl, elid)
            headers['Cookie'] = cookie
            r = client.request(u, post=post, headers=headers, cookie=cookie, XHR=True)
            r = str(json.loads(r))
            r = re.findall('\'(http.+?)\'', r) + re.findall('\"(http.+?)\"', r)
            for i in r:
                if 'google' in i:
                    quality = 'SD'
                    if 'googleapis' in i:
                        quality = source_utils.check_sd_url(i)
                    elif 'googleusercontent' in i:
                        i = directstream.googleproxy(i)
                        quality = directstream.googletag(i)[0]['quality']
                    sources.append({'source': 'gvideo', 'quality': quality, 'language': 'en', 'url': i, 'direct': True, 'debridonly': False})
                elif 'llnwi.net' in i or 'vidcdn.pro' in i:
                    quality = source_utils.check_sd_url(i)
                    sources.append({'source': 'CDN', 'quality': quality, 'language': 'en', 'url': i, 'direct': True, 'debridonly': False})
                else:
                    valid, hoster = source_utils.is_host_valid(i, hostDict)
                    if valid:
                        quality = source_utils.check_sd_url(i)
                        if 'vidnode.net' in i:
                            i = i.replace('vidnode.net', 'vidcloud9.com')
                            hoster = 'vidcloud9'
                        sources.append({'source': hoster, 'quality': quality, 'language': 'en', 'url': i, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---SHOWBOX Testing - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        if 'google' in url and not 'googleapis' in url:
            return directstream.googlepass(url)
        else:
            return url
