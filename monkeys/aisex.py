# -*- coding: utf-8 -*-
__author__ = 'peter'

import requests
from bs4 import BeautifulSoup
from cheekpouch import spawn
import re

baseurl = 'http://bt.aisex.com/bt/'


def lemons():
    aisex = (baseurl + 'thread.php?fid=4&search=&page=' + str(i) for i in range(1, 0, -1))
    for url in aisex:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        tags = soup.find_all('a', target="_blank")
        for tag in tags:
            if tag.parent.name == 'h3':
                yield baseurl + tag['href']


def harvest():
    for lemon in lemons():
        r = requests.get(lemon)
        soup = BeautifulSoup(r.text, "html.parser")
        tags = soup.find_all('a', href=re.compile("www.jandown.com"))
        for tag in tags:
            print(tag['href'])
            break
                #     for juice in juices:
                #         try:
                #             juice = Juice(key_name=lemon, image=juice['image'], download=juice['download'])
                #             juice.put()
                #         except BadValueError:
                #             logging.info(juice)
                #     bucket.append(lemon)
                # squeezed.put()


if __name__ == "__main__":
    harvest()
