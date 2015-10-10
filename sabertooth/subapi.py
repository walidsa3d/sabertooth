# -*- coding: utf-8 -*-

from providers import opensubtitles

opensubtitles = opensubtitles()


def search(queryString, lang, maxnumber, provider):
    if provider == "opensubtitles":
        return opensubtitles.query(queryString, maxnumber, "en")


def download_subtitle(url, provider):
    if provider == "opensubtitles":
        opensubtitles.download_subtitle(url)
