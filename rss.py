# -*- coding: utf-8 -*-
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib3
from bs4 import BeautifulSoup
import os
import shutil
import datetime
import re
import feedparser
import codecs

def requests_retry_session(
    retries=50,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

zurl = 'http://zelka.org/rss.php'
zcookies = {
    'uid': '',
    'pass': '',
           }
zr = requests_retry_session().get(zurl, cookies=zcookies)
#print (r.text)

zsoup = BeautifulSoup(zr.text.encode('utf-8'), 'html.parser').prettify()
#print soup

zNewsFeed = feedparser.parse(zr.text)
#entry = NewsFeed.entries[0]
for entry in zNewsFeed.entries:

    ztitle = entry.title.replace('&amp;','&')
    #print 'ztitle: '+ztitle
    #print 'zlink: '+entry.link
    zwebpage = entry.link
    zstrwp = str(zwebpage)
    #print 'zwebpage: '+zwebpage

    zs = requests.Session()
    zr2 = zs.post(zwebpage, cookies=zcookies)
    zsoup2 = BeautifulSoup(zr2.text.encode('utf-8'), 'html.parser')

    for link in zsoup2.find_all('a', limit = 35):
        znewlink = link.get('href')
    #print 'znewlink: '+znewlink
    #print soup2

    if znewlink != 'http://img2.zamunda.se/pic/chart.png':
        zelementtitle = zsoup2.find(text='Download')
        #1253 encoding to bypass zztitles with Russian and replace it with ??? characters
        zttitle0 = zelementtitle.find_next('td').text.encode('windows-1253', 'replace')
        print 'ztitle0='+zttitle0
        zttitle0 = ''.join([char if ord(char) < 128 else '' for char in zttitle0])
        zttitle = str(zttitle0).replace('.torrent','').encode('utf-8')
        #print zttitle
        element = zsoup2.find(text='Добавено')
        zpub0 = element.find_next('td').text
        zpub = str(element.find_next('td').text)
        #print zpub
        d = datetime.datetime.strptime(zpub, '%Y-%m-%d %H:%M:%S')
        dtm = d.strftime("%a, %d %b %Y %H:%M:%S %z")+'+0300'
        #print dtm

    zstrnl = str(znewlink)

    #print zsoup2
    print ztitle
    print zttitle
#    print zstrwp
    print zstrnl
    print dtm
    
    zsoup = (zsoup.replace('<title>\n    '+ztitle+'\n   </title>','<title>\n    '+'[Z] '+ztitle+' --- '+zttitle+'\n   </title>').replace(zstrwp,zstrnl+'\n   <pubDate>\n     '+dtm+'\n   </pubDate>\n   <guid>'+zstrnl+'</guid>').replace('http://img2.zamunda.se/pic/chart.png','')).replace(' </channel>\n</rss>','').replace('<rss version="0.91">','<rss version="2.00">').replace('<title>\n   Zelka.ORG\n  </title>','<title>\n   Zelka-Arena RSS Magnet Feed\n  </title>').replace('windows-1251','utf-8').replace('&amp;','&')
#print zsoup


'''
aurl = 'https://arenabg.ch/rss.php'
acookies = {
    'uid': '',
    'pass': '',
    'lang': '',
    '__auc': '',
    'SESSID': '',
    '__utmc': '',
    '__utmt': '',
    '__utma': '',
    '__utmz': '',
    '__utmb': '',
           }
ar = requests_retry_session().get(aurl, cookies=acookies, verify=True)
arcode = ar.status_code
#print(arcode)
#print (ar.text)
if arcode == 200:
    asoup = BeautifulSoup(ar.text.encode('utf-8'), 'html.parser').prettify()
    #print asoup

    aNewsFeed = feedparser.parse(ar.text)
    #entry = NewsFeed.entries[0]
    for entry in aNewsFeed.entries:

    
        #print 'akeys: '
        #print entry.keys()
        atitle = entry.title
        #print atitle
        #print 'atitle: '+atitle
        print 'alink: '+entry.link
        awebpage = entry.link
        astrwp = str(awebpage)
        #print 'awebpage: '+awebpage
        print 'apublished: '+entry.published


        ars = requests.Session()
        aresponse = ars.get(awebpage, cookies=acookies, verify=True)
        #print(aresponse.text)[0:400]
        asoup2 = BeautifulSoup(aresponse.text.encode('utf-8'), 'html.parser')
        #print asoup2

        for link in asoup2.find_all('a', limit = 30):
            anewlink0 = link.get('href')
            if anewlink0 and (anewlink0.startswith("magnet")):
                anewlink = anewlink0
                print 'anewlink: '+anewlink
        #print asoup2

        astrnl = str(anewlink)
        asoup = asoup.replace(atitle,'[A] '+atitle).replace(astrwp,astrnl).replace('<?xml version="1.0" encoding="utf-8"?>\n<rss version="2.0">\n <channel>\n  <title>\n   ArenaBG.com rss feed\n  </title>\n  <link/>\n  https://arenabg.com\n  <description>\n   ArenaBG.com rss feed\n  </description>\n  <language>\n   en-us\n  </language>\n  <copyright>\n   Copyright (C) 2019 ArenaBG.com\n  </copyright>','').replace('&amp;','&')
    #print asoup

    soup = zsoup+asoup
    #print soup
'''
path = os.path.abspath("PATHTOSAVETHEXMLFILE/rss.xml")
f = codecs.open(path, "w", "utf-8")
f.write(zsoup)
f.close()
