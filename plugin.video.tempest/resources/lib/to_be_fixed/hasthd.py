import re
import requests
import xbmc
from resources.lib.modules import cleantitle
from bs4 import BeautifulSoup

class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['http://dl.hastidl.net']
        self.base_link = 'http://dl.hastidl.net/remotes/'
        sources = []

    def movie(self, title, year, imdb):
        sources = []
        try:
            url = self.base_link
            html = requests.get(url, timeout=5).content
            match = re.compile('<a href="(.+?)">(.+?)</a>').findall(html)
            for url,name in match:
                new_title = name.split('20')[0]
                if cleantitle.get(title).lower()==cleantitle.get(new_title).lower():
                    if year in url:
                        url = self.base_link+url
                        if '3D' in url:                                          
                            qual = '3D'
                        elif '1080p' in url:
                            qual = '1080p'
                        elif '720p' in url: 
                            qual = '720p'
                        elif '480p' in url:
                            qual = '480p'
                        else:
                            qual = 'SD'
                        sources.append({'source': 'Direct', 'quality': qual, 'url': url,'direct': True, 'debrid': False})
            return sources
        except:
            return url

    def episode(self, title, year, season, episode, imdb, tvdb):
        sources = []
        try:
            url = self.base_link
            html = requests.get(url,timeout=5).content
            match = re.compile('<a href="(.+?)">(.+?)</a>').findall(html)
            for url,name in match:
                if cleantitle.get(title.lower()) in cleantitle.get(name.lower()):

                    if len(season)==1:
                        season = '0'+season
                    if len(episode)==1:
                        episode = '0'+episode

                    episode_chk = 's%se%s' %(season,episode)
                    if episode_chk.lower() in url.lower():
                        if '1080p' in url:
                            qual = '1080p'
                        elif '720p' in url:
                            qual = '720p'
                        elif '560p' in url:
                            qual = '560p'
                        elif '480p' in url:
                            qual = '480p'
                        else:
                            qual = 'SD'
                        url = self.base_link+url
                        sources.append({'source': 'Direct', 'quality': qual, 'url': url, 'direct': True, 'debridonly': False})
            return sources
        except:
            return url

    def sources(self, url, hostDict, hostprDict):
        return url

    def resolve(self, url):
            return url