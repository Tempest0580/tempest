import requests
import sys
import bs4 as bs
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

base_link = 'http://123hulu.unblockall.org/'
search_link = 'search-movies/%s.html' % search
title = 'spider-man'


clean_title = geturl(title).replace(' ','-')
url = base_link + search_link
scraper = cfscrape.create_scraper()
r = scraper.get(url)
r = s(r.text, 'html.parser').find_all('div', class_="ml-item")
for i in r:
    link = i.find_all('a')
    for url in link:
            print url['href']

#url = requests.get(url)

#print url