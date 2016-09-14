# -*- coding: utf-8 -*-
__author__ = 'peter'


from .cheekpouch import r

def spawn_torrent(url):
    torrent = r.hgetall(url)
    if torrent:
        return torrent
    else:
        torrent = {'status': 'MISS'}
        return torrent
