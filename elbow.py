# -*- coding: utf-8 -*-
__author__ = 'peter'

from monkeys import spawn_torrent, twentyfour_seven, week, hour
from settings import settings

import tornado.ioloop
import tornado.web
import json


class GreaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('grease.html')

    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        if data:
            torrent = spawn_torrent(data['url'])
            self.write(torrent)


class TwentyFourSevenHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(list(twentyfour_seven())))


class HourHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(hour()))


class WeekHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(week()))


def make_app():
    return tornado.web.Application([
        (r"/grease/168\.json", TwentyFourSevenHandler),
        (r"/grease/hour\.json", HourHandler),
        (r"/grease/week\.json", WeekHandler),
        (r"/grease", GreaseHandler),
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
