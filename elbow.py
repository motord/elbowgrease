# -*- coding: utf-8 -*-
__author__ = 'peter'

from bottle import Bottle, run, template, request
import bottle

import hashlib
from bt import BTFailure, bdecode, bencode
from dropbox import download_torrent

bottle.debug(mode=True)
app = Bottle()

@app.route('/grease', method="POST")
def fetch():
    data = request.json
    if data:
        torrent = download_torrent(data['url'])
        try:
            metainfo = bdecode(torrent)
            info = metainfo['info']
            btih=hashlib.sha1(bencode(info)).hexdigest()
            dn=metainfo['info']['name']
            link=template('magnet:?xt=urn:btih:{{btih}}&dn={{dn}}', btih=btih, dn=dn)
            return {'status': 'OK',  'link': link}
        except BTFailure:
            return {'status': 'ERROR', 'error': 'not a valid .torrent file'}

app.run(host='localhost', port=8080)