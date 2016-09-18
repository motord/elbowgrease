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
from datetime import datetime
import json
from functools import partial, reduce

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


def events_matching_type_during(start, end, type):
    events = events_matching_type_during_lua(keys=['events'], args=[start, end, type])
    return json.loads(events)


events_matching_type_during_lua = r.register_script('''
local events = {}
local ids = redis.call('ZRANGEBYSCORE', KEYS[1], ARGV[1], ARGV[2])
for i, id in ipairs(ids) do
    local event = redis.call('HMGET', 'event:' .. id, 'type', 'timestamp')
    if event[1]==ARGV[3] then
        events[i] = event[2]
    end
end

return cjson.encode(events)
''')


def events_matching_type(type):
    events = events_matching_type_lua(keys=['events'], args=[type])
    return json.loads(events)


events_matching_type_lua = r.register_script('''
local events = {}
local ids = redis.call('ZRANGE', KEYS[1], 0, -1)
for i, id in ipairs(ids) do
    local event = redis.call('HMGET', 'event:' .. id, 'type', 'timestamp')
    if event[1]==ARGV[1] then
        events[i] = event[2]
    end
end

return cjson.encode(events)
''')


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
    event['timestamp'] = time.time()
    event_key = 'event:{id}'.format(id=id)

    pipe = r.pipeline(True)
    pipe.hmset(event_key, event)
    pipe.zadd('events', **{str(id): event['timestamp']})
    pipe.execute()


def twentyfour_seven():
    return map(lambda e: {'x': datetime.fromtimestamp(float(e)).strftime('%F'), \
                          'y': datetime.fromtimestamp(float(e)).strftime('%R')}, \
               events_matching_type_during(time.time() - 86400 * 7, time.time(), 'aisex.newtorrent'))


def week():
    func=lambda e: datetime.fromtimestamp(float(e)).strftime('%A')
    return reduce(partial(rollup_by_function, func=func), events_matching_type('aisex.newtorrent'),{})


def hour():
    func=lambda e: datetime.fromtimestamp(float(e)).strftime('%k')
    return reduce(partial(rollup_by_function, func=func), events_matching_type('aisex.newtorrent'),{})

def rollup_by_function(accum, x, func=None):
    try:
        key=func(x)
        accum[key]=accum[key]+1
    except KeyError:
        accum[key]=1
    return accum