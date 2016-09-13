# -*- coding: utf-8 -*-
__author__ = 'peter'

from monkeys import spawn_torrent

import tornado.ioloop
import tornado.web
import json

class GreaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        if data:
            torrent = spawn_torrent(data['url'])
            self.write(torrent)

def make_app():
    return tornado.web.Application([
        (r"/grease", GreaseHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()