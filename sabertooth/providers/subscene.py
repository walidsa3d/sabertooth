# -*- coding: utf-8 -*-

import zipfile

from itertools import chain

import requests

import cStringIO

from bs4 import BeautifulSoup as BS


class Subscene(object):

    def __init__(self):
        self.base_url = 'http://subscene.com'
        self.language = 'english'
        self.headers = {}

    def search(self, release_name):
        """search subtitles from subscene.com"""
        subtitles = []
        payload = {'q': release_name, 'r': 'true'}
        url = 'http://subscene.com/subtitles/release'
        response = requests.get(url, params=payload, headers=self.headers).text
        soup = BS(response, "lxml")
        positive = soup.find_all(class_='l r positive-icon')
        neutral = soup.find_all(class_='l r neutral-icon')
        for node in chain(positive, neutral):
            suburl = node.parent['href']
            quality = node['class'][2].split('-')[0]
            name = node.parent.findChildren()[1].text.strip()
            if self.language in suburl and 'trailer' not in name.lower():
                subtitles.append(
                    {'url': self.base_url+suburl, 'name': name, 'quality': quality})
        return subtitles

    def download(self, sub_url):
        """download and unzip subtitle archive to a temp location"""
        response = requests.get(sub_url, headers=self.headers).text
        soup = BS(response, 'lxml')
        downlink = self.base_url+soup.select('.download a')[0]['href']
        data = requests.get(downlink, headers=self.headers)
        z = zipfile.ZipFile(cStringIO.StringIO(data.content))
        srt_files = [f.filename for f in z.filelist
                     if f.filename.rsplit('.')[-1].lower() in ['srt', 'ass']]
        z.extract(srt_files[0], '/tmp/')
        return srt_files[0]
