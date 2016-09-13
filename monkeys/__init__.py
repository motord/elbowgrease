# -*- coding: utf-8 -*-
__author__ = 'peter'

import hashlib
import mechanicalsoup
import redis
import dropbox
from bencodepy import decode, encode


browser=mechanicalsoup.Browser()

def download_torrent(url):
    page = browser.get(url)

    # page.soup is a BeautifulSoup object http://www.crummy.com/software/BeautifulSoup/bs4/doc/#beautifulsoup
    # we grab the form
    form = page.soup.select("form")[0]

    # submit form
    response = browser.submit(form, page.url)
    return response.content


r = redis.StrictRedis(host='localhost', port=6379, db=0)

def spawn_torrent(url):
    torrent = download_torrent(url)
    dbx=dropbox.Dropbox('JUEnSrL_pnAAAAAAAAAACjwtIHCP7-quP8fVqMwlYeARJpkUqDzpfN5JWQV3d0ps')
    try:
        metainfo = decode(torrent)
        info = metainfo[b'info']
        btih=hashlib.sha1(encode(info)).hexdigest()
        dn=metainfo[b'info'][b'name']
        link='magnet:?xt=urn:btih:{btih}&dn={dn}'.format(btih=btih, dn=dn)
        return {'status': 'OK',  'link': link}
    except :
        return {'status': 'ERROR', 'error': 'not a valid torrent file'}
