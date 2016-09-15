# -*- coding: utf-8 -*-
__author__ = 'peter'

import requests
from bs4 import BeautifulSoup
from cheekpouch import spawn, r
import re
from rq import Queue

baseurl = 'http://bt.aisex.com/bt/'
q = Queue(connection=r)


def lemons():
    aisex = (baseurl + 'thread.php?fid=4&search=&page=' + str(i) for i in range(1, 0, -1))
    for url in aisex:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        tags = soup.find_all('a', target="_blank")
        for tag in tags:
            if tag.parent.name == 'h3':
                yield baseurl + tag['href']


def harvest():
    for lemon in lemons():
        response = requests.get(lemon)
        soup = BeautifulSoup(response.text, "html.parser")
        tags = soup.find_all('a', href=re.compile("www.jandown.com"))
        for tag in tags:
            url = tag['href']
            if r.hgetall(url):
                pass
            else:
                q.enqueue(spawn, url)
            break


if __name__ == "__main__":
    harvest()
