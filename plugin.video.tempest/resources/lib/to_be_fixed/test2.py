import requests
from bs4 import BeautifulSoup as bs

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['seriescr.com']
        self.base_link = 'http://seriescr.com'
        self.search_link = '/?s=%s'

    def query(title):
        if title is None: return
        title = title.replace('\'', '').rsplit(':', 1)[0].rsplit(' -', 1)[0].replace('-', ' ')
        return title

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'title': title, 'year': year}
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if len(episode) == 1:
                episode = "0" + episode
            if len(season) == 1:
                season = "0" + season
            url = {'tvshowtitle': url, 'season': season, 'episode': episode}
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            with requests.Session() as s:
                if 'episode' in url:
                    link = self.query(url['tvshowtitle']) + ".s" + url['season'] + "e" + url['episode']
                else:
                    link = self.query("%s.%s") % (url['title'], url['year'])
                    p = s.get(self.search_link + link)
                    soup = bs(p.content, 'html.parser')
                    soup = soup.find_all('h2', class_='entry-title')

                    #sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                    #                'direct': False, 'debridonly': True})

            return sources
        except:
            return sources

    def resolve(self, url):
        return url
