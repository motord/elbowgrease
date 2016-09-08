# -*- coding: utf-8 -*-
__author__ = 'peter'

import mechanicalsoup


def download_torrent(url):
    br=mechanicalsoup.Browser()
    page = br.get(url)

    # page.soup is a BeautifulSoup object http://www.crummy.com/software/BeautifulSoup/bs4/doc/#beautifulsoup
    # we grab the form
    form = page.soup.select("form")[0]

    # submit form
    response = br.submit(form, page.url)
    return response._content