# -*- coding: utf-8 -*-
__author__ = 'peter'

import hashlib
import mechanicalsoup
import redis
import dropbox
from bencodepy import decode, encode
from urllib.parse import urlparse
import re

browser = mechanicalsoup.Browser()


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
    torrent = r.get(url)
    if torrent:
        return torrent
    else:
        torrent_url_components = urlparse(url)
        torrent_url_query = torrent_url_components.query
        match = re.search('ref=(.*)', torrent_url_query)
        if match is None:
            pass
        else:
            torrent_file = str(match.groups(0)[0]) + '.torrent'
            blob = download_torrent(url)
            dbx = dropbox.Dropbox('JUEnSrL_pnAAAAAAAAAADGNPxjjbk3nYLnatbTN8vvJ01JM8yQIhn-MI5DqW41nR')
            dbx.files_upload(blob, '/torrents/%s' % torrent_file)
            try:
                metainfo = decode(blob)
                info = metainfo[b'info']
                btih = hashlib.sha1(encode(info)).hexdigest()
                dn = metainfo[b'info'][b'name']
                magnet = 'magnet:?xt=urn:btih:{btih}&dn={dn}'.format(btih=btih, dn=dn)
                link = ''
                torrent = {'status': 'OK', 'magnet': magnet, 'torrent': link}
                r.set(url, torrent)
                return torrent
            except:
                torrent = {'status': 'ERROR', 'error': 'not a valid torrent file'}
                return torrent
