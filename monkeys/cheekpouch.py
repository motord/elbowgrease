# -*- coding: utf-8 -*-
__author__ = 'peter'

import hashlib
import mechanicalsoup
import redis
import dropbox
from bencodepy import decode, encode
from urllib.parse import urlparse
import re
import time

browser = mechanicalsoup.Browser()


def download_torrent(url):
    page = browser.get(url)

    # page.soup is a BeautifulSoup object http://www.crummy.com/software/BeautifulSoup/bs4/doc/#beautifulsoup
    # we grab the form
    form = page.soup.select("form")[0]

    # submit form
    response = browser.submit(form, page.url)
    return response.content


r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def spawn(url):
    torrent_url_components = urlparse(url)
    torrent_url_query = torrent_url_components.query
    match = re.search('ref=(.*)', torrent_url_query)
    if match is None:
        pass
    else:
        torrent_file = str(match.groups(0)[0]) + '.torrent'
        blob = download_torrent(url)
        dbx = dropbox.Dropbox('JUEnSrL_pnAAAAAAAAAADGNPxjjbk3nYLnatbTN8vvJ01JM8yQIhn-MI5DqW41nR')
        path = '/torrents/%s' % torrent_file
        dbx.files_upload(blob, path)
        link = dbx.sharing_create_shared_link_with_settings(path).url
        link = re.sub('dl=0', 'dl=1', link)
        try:
            metainfo = decode(blob)
            info = metainfo[b'info']
            btih = hashlib.sha1(encode(info)).hexdigest()
            dn = metainfo[b'info'][b'name']
            magnet = 'magnet:?xt=urn:btih:{btih}&dn={dn}'.format(btih=btih, dn=dn)
            torrent = {'status': 'OK', 'magnet': magnet, 'torrent': link}
            r.hmset(url, torrent)
            record_event({'type': 'aisex.newtorrent'})
            return torrent
        except:
            torrent = {'status': 'ERROR', 'error': 'not a valid torrent file'}
            return torrent


def record_event(event):
    id = r.incr('event:id')
    event['id'] = id
    event['timestamp'] = time.localtime()
    event_key = 'event:{id}'.format(id=id)

    pipe = r.pipeline(True)
    pipe.hmset(event_key, event)
    pipe.zadd('events', **{id: event['timestamp']})
    pipe.execute()
