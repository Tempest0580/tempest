import requests
import sys
from bs4 import BeautifulSoup as bs
import cfscrape
import re
import time
from bs4 import BeautifulSoup as s

User_Agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4'


def check_sd_url(release_link):
    try:
        release_link = release_link.lower()
        if '1080' in release_link: quality = '1080p'
        elif '720' in release_link: quality = '720p'
        elif '.hd.' in release_link: quality = '720p'
        elif any(i in ['dvdscr', 'r5', 'r6'] for i in release_link): quality = 'SCR'
        elif any(i in ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'telesync', 'ts'] for i in release_link): quality = 'CAM'
        else: quality = 'SD'
        return quality
    except:
        return 'SD'

def geturl(title):
    if title is None: return
    title = title.lower()
    title = title.translate(None, ':*?"\'\.<>|&!,')
    title = title.replace('/', '-')
    title = title.replace(' ', '-')
    title = title.replace('--', '-')
    return title


headers = {'User_Agent = Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4'}
search = 'arrow season 6 episode 13'

base_link = 'http://crazy4tv.com'
search_link = '/search/the flash s04e15'
sources= []

url = base_link + search_link.replace(' ', '+')
scraper = cfscrape.create_scraper()
r = scraper.get(url).text
r = bs(r, 'html.parser')
link = r.find_all('p', style="text-align: center;")

for i in link:
    s = i.find_all('strong')
    for url in s:
        p = url.find_all('a', href=True)
        for url in p:
            host = url.text
            url = url['href']

            sources.append(
                {'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': True})
        print  sources