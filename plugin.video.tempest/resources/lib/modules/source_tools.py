# Original file: schism_meta and code bits from others.
# Contents: all sorts of random code for source work lol.

import re, urllib, urlparse
import requests, time
import HTMLParser

RES_8K   =  ['8k', 'hd8k', '8khd', '4320p', '4320i', 'hd4320', '4320hd', '5120p', '5120i', 'hd5120', '5120hd', '8192p', '8192i', 'hd8192', '8192hd']
RES_6K   =  ['6k', 'hd6k', '6khd', '3160p', '3160i', 'hd3160', '3160hd', '4096p', '4096i', 'hd4096', '4096hd']
RES_4K   =  ['4k', 'hd4k', '4khd', 'uhd', 'ultrahd', 'ultra hd', 'ultra high', '2160', '2160p', '2160i', 'hd2160', '2160hd', '1716p', '1716i', 'hd1716', '1716hd', '2664p', '2664i', 'hd2664', '2664hd', '3112p', '3112i', 'hd3112', '3112hd', '2880p', '2880i', 'hd2880', '2880hd']
RES_2K   =  ['2k', 'hd2k', '2khd', '2048p', '2048i', 'hd2048', '2048hd', '1332p', '1332i', 'hd1332', '1332hd', '1556p', '1556i', 'hd1556', '1556hd']
RES_1080 =  ['1080', '1080p', '1080i', 'hd1080', '1080hd', '1200p', '1200i', 'hd1200', '1200hd']
RES_HD   =  ['720', '720p', '720i', 'hd720', '720hd', 'hd']
RES_SD   =  ['576', '576p', '576i', 'sd576', '576sd', '480', '480p', '480i', 'sd480', '480sd', '360', '360p', '360i', 'sd360', '360sd', '240', '240p', '240i', 'sd240', '240sd']
SCR =  ['dvdscr', 'screener', 'scr', 'r5', 'r6']
CAM =  ['camrip', 'cam rip', 'tsrip', 'ts rip', 'hdcam', 'hd cam', 'hdts', 'hd ts', 'dvdcam', 'dvd cam', 'dvdts', 'dvd ts', 'cam', 'telesync', 'tele sync', 'ts']

CODEC_H265 = ['hevc', 'h265', 'x265', '265']
CODEC_H264 = ['avc', 'h264', 'x264', '264']
CODEC_XVID = ['xvid']
CODEC_DIVX = ['divx', 'div2', 'div3']
CODEC_MPEG = ['mp4', 'mpeg', 'm4v', 'mpg', 'mpg1', 'mpg2', 'mpg3', 'mpg4', 'msmpeg', 'msmpeg4', 'mpegurl']
CODEC_AVI  = ['avi']
CODEC_MKV  = ['mkv', 'matroska']

AUDIO_8CH = ['ch8', '8ch', 'ch7', '7ch', '7 1', 'ch7 1', '7 1ch']
AUDIO_6CH = ['ch6', '6ch', 'ch6', '6ch', '6 1', 'ch6 1', '6 1ch', '5 1', 'ch5 1', '5 1ch']
AUDIO_2CH = ['ch2', '2ch', 'stereo', 'dualaudio', 'dual', '2 0', 'ch2 0', '2 0ch']
AUDIO_1CH = ['ch1', '1ch', 'mono', 'monoaudio', 'ch1 0', '1 0ch']

VIDEO_3D = ['3d', 'sbs', 'hsbs', 'sidebyside', 'side by side', 'stereoscopic', 'tab', 'htab', 'topandbottom', 'top and bottom']


def name_clean(name):
    name = HTMLParser.HTMLParser().unescape(name)
    name = name.replace('&quot;', '\"')
    name = name.replace('&amp;', '&')
    name = name.strip()
    return name


def url_clean(url):
    url = HTMLParser.HTMLParser().unescape(url)
    url = url.replace('&quot;', '\"')
    url = url.replace('&amp;', '&')
    url = url.strip()
    return url


def get_host(url):
    try:
        host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]
    except:
        elements = urlparse.urlparse(url)
        host = elements.netloc
    return host.replace('www.', '')


def get_codec(txt):
    txt = txt.lower()
    if any(value in txt for value in CODEC_H265):
        txt = "HEVC | "
    elif any(value in txt for value in CODEC_MKV):
        txt = "MKV | "
    elif any(value in txt for value in CODEC_DIVX):
        txt = "DIVX | "
    elif any(value in txt for value in CODEC_MPEG):
        txt = "MPEG | "
    elif any(value in txt for value in CODEC_XVID):
        txt = "XVID | "
    elif any(value in txt for value in CODEC_AVI):
        txt = "AVI | "
    else:
        txt = '0'
    return txt


def get_audio(txt):
    txt = txt.lower()
    if any(value in txt for value in AUDIO_8CH):
        txt = "7.1 "
    elif any(value in txt for value in AUDIO_6CH):
        txt = "5.1 "
    elif any(value in txt for value in AUDIO_2CH):
        txt = "2.0 "
    elif any(value in txt for value in AUDIO_1CH):
        txt = "Mono "
    else:
        txt = '0'
    return txt


def get_size(txt):
    txt = txt.lower()
    try:
        txt = re.findall('(\d+(?:\.|/,|)?\d+(?:\s+|)(?:gb|GiB|mb|MiB|GB|MB))', txt)
        txt = txt[0].encode('utf-8')
        txt = txt + " | "
    except:
        txt = '0'
    return txt


def get_3D(txt):
    txt = txt.lower()
    if any(value in txt for value in VIDEO_3D):
        txt = "3D | "
    else:
        txt = '0'
    return txt


def get_gvideo_quality(url):
    quality = re.compile('itag=(\d*)').findall(url)
    quality += re.compile('=m(\d*)$').findall(url)
    try: 
        quality = quality[0]
    except:
        quality = "ND"
        return quality
    if quality in ['37', '137', '299', '96', '248', '303', '46']:
        quality = "1080p"
        return quality
    elif quality in ['22', '84', '136', '298', '120', '95', '247', '302', '45', '102']:
        quality = "HD"
        return quality
    elif quality in ['35', '44', '135', '244', '94']:
        quality = "SD"
        return quality
    elif quality in ['18', '34', '43', '82', '100', '101', '134', '243', '93']:
        quality = "SD"
        return quality
    elif quality in ['5', '6', '36', '83', '133', '242', '92', '132']:
        quality = "SD"
        return quality
    else:
        quality = "SD"
        return quality


def get_quality(txt, txt2=''):
    txt = txt.lower()
    if not txt2 == '':
        txt = txt.lower() + ' ' + txt2.lower()
    if any(value in txt for value in RES_4K):
        quality = "4K"
    elif any(value in txt for value in RES_2K):
        quality = "2K"
    elif any(value in txt for value in RES_1080):
        quality = "1080p"
    elif any(value in txt for value in RES_HD):
        quality = "720p"
    elif any(value in txt for value in RES_SD):
        quality = "SD"
    else:
        quality = "SD"
    return quality


def get_info(txt, txt2=''):
    txt = txt.lower()
    if not txt2 == '':
        txt = txt.lower() + ' ' + txt2.lower()
    info = ''
    codec = get_codec(txt)
    audio = get_audio(txt)
    size = get_size(txt)
    video3d = get_3D(txt)	
    if codec == '0' or codec == '':
        codec = ''
    if audio == '0' or audio == '':
        audio = ''
    if size == '0' or size == '':
        size = ''
    if video3d == '0' or video3d == '':
        video3d = ''			
    info = video3d + size + codec + audio
    return info	


def checkHost(url, hostList):
    host = get_host(url)
    validHost = False
    for i in hostList:
        if i.lower() in url.lower():
            host = i
            validHost = True
            return validHost, host
    return validHost, host


def check_site(host):
    try:
        Resolve = ['downace', 'gorillavid', 'yourupload', 'entervideo', 'vimeo',
            'vidoza', 'clicknupload', 'estream', 'vidnode', 'vidzi', 'putload',
            'mp4upload', 'trollvid', 'vidstreaming', 'dailymotion', 'blazefile',
            'uptostream', 'uptobox', 'vidcloud', 'vcstream', 'vidto', 'flashx', 
            'vshare', 'vidup', 'xstreamcdn', 'vev', 'xvidstage', 'thevideo'
        ]
        Debrid = ['1fichier', 'rapidgator', 'userscloud', 'vidlox', 'filefactory',
            'turbobit', 'nitroflare'
        ]
        if host in Resolve:
            return host + 'Resolve'
        elif host in Debrid:
            return host + 'Debrid'
        return host
    except:
        return


websites = set()
def check_dupes(url):
    from urlparse import urlparse
    parsed = urlparse(url)
    website = parsed.hostname + parsed.path
    if website in websites:
        return False
    websites.add(website)
    return True


def check_playable(url):
    try:
        headers = url.rsplit('|', 1)[1]
    except:
        headers = ''
    headers = urllib.quote_plus(headers).replace('%3D', '=') if ' ' in headers else headers
    headers = dict(urlparse.parse_qsl(headers))
    result = None
    try:
        if url.startswith('http') and '.m3u8' in url:
            result = requests.head(url.split('|')[0], headers=headers, timeout=5)
            if result is None:
                return None
        elif url.startswith('http'):
            result = requests.head(url.split('|')[0], headers=headers, timeout=5)
            if result is None:
                return None
    except:
        pass
    return result


