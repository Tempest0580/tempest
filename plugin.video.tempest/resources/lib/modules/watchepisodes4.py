
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

import re
import urllib
import requests
import cleantitle

User_Agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4'


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['watchepisodes4.com']
        self.base_link = 'http://www.watchepisodes4.com'
        self.search_link = 'search/ajax_search?q=%s'

    def episode(self, title, show_year, year, season, episode, imdb, tvdb):
        try:
            scrape = cleantitle.getsearch(title.lower())
            start_url = '%ssearch/ajax_search?q=%s' % (self.base_link, scrape)
            headers = {'User_Agent': User_Agent}
            html = requests.get(start_url, headers=headers, timeout=5).content
            regex = re.compile('"value":"(.+?)","seo":"(.+?)"', re.DOTALL).findall(html)
            for name, link_title in regex:
                if not cleantitle.get(title).lower() == cleantitle.get(name).lower():
                    continue
                show_page = self.base_link + link_title

                format_grab = 'season-%s-episode-%s-' % (season, episode)
                headers = {'User_Agent': User_Agent}
                linkspage = requests.get(show_page, headers=headers, timeout=5).content
                series_links = re.compile('<div class="el-item.+?href="(.+?)"', re.DOTALL).findall(linkspage)
                for url in series_links:
                    if not format_grab in url:
                        continue
                    return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            hostDict = hostprDict + hostDict
            headers = {'User_Agent': User_Agent}
            links = requests.get(url, headers=headers, timeout=5).content
            LINK = re.compile('<div class="link-number".+?data-actuallink="(.+?)"', re.DOTALL).findall(links)

            for url in LINK:
                host = url.split('//')[1].replace('www.', '')
                host = host.split('/')[0].lower()
                if not hostDict(host):
                    continue
                host = host.split('.')[0].title()
                sources.append(
                    {'source': host, 'quality': 'DVD', 'url': url, 'direct': False, 'debrid': False})
        except:
            pass