# -*- coding: utf-8 -*-
import gzip
import os
import shutil
import xmlrpclib

import babelfish
import requests


class opensubtitles(object):

    def __init__(self):
        self.api_url = 'http://api.opensubtitles.org/xml-rpc'

    def download_subtitle(self, subtitle):
        suburl = subtitle["link"]
        videofilename = subtitle["release"]
        srtbasefilename = videofilename.rsplit(".", 1)[0]
        response = requests.get(suburl, stream=True)
        zip_filename = srtbasefilename+".srt.gz"
        with open(zip_filename, 'wb') as out_file:
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
        search = {}
        subtitles = []
        if moviehash:
            search['moviehash'] = moviehash
        if imdbID:
            search['imdbid'] = imdbID
        if bytesize:
            search['moviebytesize'] = str(bytesize)
        if len(search) == 0:
            search['query'] = filename
        server = xmlrpclib.Server(self.api_url)
        try:
            login_result = server.LogIn("", "", "eng", "periscope")
            token = login_result["token"]
        except Exception:
            print "Login Error"
            return subtitles
        results = server.SearchSubtitles(token, [search])
        if results['data']:
            for r in results['data']:
                subtitle = {}
                subtitle["release"] = r['SubFileName']
                subtitle["link"] = r['SubDownloadLink']
                subtitle["lang"] = r['SubLanguageID']
                subtitle["movie"] = r['MovieReleaseName']
                subtitle["date"] = r['SubAddDate']
                subtitles.append(subtitle)
        try:
            server.LogOut(token)
        except:
            print "Logout Error"
        lang = babelfish.Language.fromalpha2(lang).opensubtitles
        results = [x for x in subtitles if x["lang"] == lang][:maxnumber]
        return results
      
