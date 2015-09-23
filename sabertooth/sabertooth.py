# -*- coding: utf-8 -*-
import commands
import gzip
import logging
import os
import shutil
import struct
import traceback
import xmlrpclib

import requests

import langs


class opensubs(object):

    def __init__(self):
        pass

    def download_subtitle(self, subtitle):
        suburl = subtitle["link"]
        videofilename = subtitle["release"]
        srtbasefilename = videofilename.rsplit(".", 1)[0]
        response = requests.get(suburl, stream=True)
        with open(srtbasefilename+".srt.gz", 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        f = gzip.open(srtbasefilename+".srt.gz")
        dump = open(srtbasefilename+".srt", "wb")
        dump.write(f.read())
        dump.close()
        f.close()
        os.remove(srtbasefilename+".srt.gz")
        return srtbasefilename+".srt"

    def query(self, filename, maxnumber, lang, imdbID=None, moviehash=None, bytesize=None):
        # Prepare the search
        search = {}
        sublinks = []
        if moviehash:
            search['moviehash'] = moviehash
        if imdbID:
            search['imdbid'] = imdbID
        if bytesize:
            search['moviebytesize'] = str(bytesize)
        if len(search) == 0:
            search['query'] = filename
        # Login
        server = xmlrpclib.Server('http://api.opensubtitles.org/xml-rpc')
        login_result = server.LogIn("", "", "eng", "periscope")
        token = login_result["token"]
        results = server.SearchSubtitles(token, [search])
        sublinks = []
        if results['data']:
            for r in results['data']:
                result = {}
                result["release"] = r['SubFileName']
                result["link"] = r['SubDownloadLink']
                result["lang"] = r['SubLanguageID']
                result["movie"] = r['MovieReleaseName']
                result["date"] = r['SubAddDate']
                sublinks.append(result)
        lang = langs.OS_LANGS[lang] if lang in langs.OS_LANGS else "eng"
        return [x for x in sublinks if x["lang"] == lang][:maxnumber]
        try:
            server.LogOut(token)
        except:
            print "Open subtitles could not be contacted for logout"
