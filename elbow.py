# -*- coding: utf-8 -*-
__author__ = 'peter'

import hashlib
from bencodepy import decode, encode
from dropbox import download_torrent

import tornado.ioloop
import tornado.web
import json

class GreaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        if data:
            torrent = download_torrent(data['url'])
            try:
                metainfo = decode(torrent)
                info = metainfo[b'info']
                btih=hashlib.sha1(encode(info)).hexdigest()
                dn=metainfo[b'info'][b'name']
                link='magnet:?xt=urn:btih:{btih}&dn={dn}'.format(btih=btih, dn=dn)
                self.write({'status': 'OK',  'link': link})
            except :
                self.write({'status': 'ERROR', 'error': 'not a valid torrent file'})

def make_app():
    return tornado.web.Application([
        (r"/grease", GreaseHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()