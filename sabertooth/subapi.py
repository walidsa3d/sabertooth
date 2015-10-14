# -*- coding: utf-8 -*-

from providers import Opensubtitles
from providers import Subscene

sites = {'opensubtitles': Opensubtitles,
         'subscene': Subscene}


def search(provider, queryString, lang='en', maxnumber=10):
    if provider in sites:
        return sites[provider]().search(queryString, maxnumber, lang)
    else:
        raise ValueError('Provider Not Supported')


def download(provider, url):
    if provider in sites:
        return sites[provider]().download(url)
    else:
        raise ValueError('Provider Not Supported')
