# -*- coding: utf-8 -*-

'''
    Tempest Add-on


    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import re,urllib,urlparse,json,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import source_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['filmxy.cc']
        self.base_link = 'http://www.filmxy.me'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url == None: return
            urldata = urlparse.parse_qs(url)
            urldata = dict((i, urldata[i][0]) for i in urldata)
            title = urldata['title'].replace(':', ' ').replace('-', ' ').lower()
            year  = urldata['year']

            search_id = title.lower()
            start_url = self.search_link % (self.base_link, search_id.replace(' ','%20'))

            headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
            html = client.request(start_url,headers=headers)
            Links = re.compile('"post","link":"(.+?)","title".+?"rendered":"(.+?)"',re.DOTALL).findall(html)
            for link,name in Links:
                link = link.replace('\\','')
                name = name.replace('&#038;', '')
                if title.lower() in name.lower(): 
                    if year in name:
                        holder = client.request(link,headers=headers)
                        dpage = re.compile('id="main-down".+?href="(.+?)"',re.DOTALL).findall(holder)[0]
                        sources = self.scrape_results(dpage, title, year)
                        return sources
            return sources
        except:
            return sources

    def scrape_results(self,url,title,year):
        sources = []
        try:
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
            html = client.request(url,headers=headers)
            
            block720 = re.compile('class="links_720p"(.+?)</ul>',re.DOTALL).findall(html)
            Links720 = re.compile('href="(.+?)"',re.DOTALL).findall(str(block720)) 
            for link in Links720:
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].lower()
                if host not in ['upload.af', 'upload.mn', 'uploadx.org']:
                    sources.append({'source':host,'quality':'720p','language': 'en','url':link,'info':[],'direct':False,'debridonly':False})

            block1080 = re.compile('class="links_1080p"(.+?)</ul>',re.DOTALL).findall(html)
            Links1080 = re.compile('href="(.+?)"',re.DOTALL).findall(str(block1080)) 
            for link in Links1080:
                host = link.split('//')[1].replace('www.','')
                host = host.split('/')[0].lower()
                if host not in ['upload.af', 'upload.mn', 'uploadx.org']:
                    sources.append({'source':host,'quality':'1080p','language': 'en','url':link,'info':[],'direct':False,'debridonly':False})

            return sources   
        except:
            return sources

    def resolve(self, url):
        return url
