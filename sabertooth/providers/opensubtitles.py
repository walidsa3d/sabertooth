# -*- coding: utf-8 -*-

import gzip
import os
import shutil
import xmlrpclib

import babelfish
import difflib
import requests

class Opensubtitles(object):

    def __init__(self):
        self.api_url = 'http://api.opensubtitles.org/xml-rpc'

    def download(self, subtitle, dldir):
        suburl = subtitle["link"]
        videofilename = subtitle["release"]
        srtbasefilename = videofilename.rsplit(".", 1)[0]
        response = requests.get(suburl, stream=True)
        zip_filename = srtbasefilename+".srt.gz"
        with open(zip_filename, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        f = gzip.open(srtbasefilename+".srt.gz")
        extracted_file = os.path.join(dldir, srtbasefilename+".srt")
        dump = open(extracted_file, "wb")
        dump.write(f.read())
        dump.close()
        f.close()
        os.remove(srtbasefilename+".srt.gz")
        return extracted_file

    def compare(self, movie, sub):
        ratio = 0
        seq = difflib.SequenceMatcher(None, movie, sub)
        ratio = ratio + seq.ratio()
        return ratio

    def best_subtitle(self, filename, langs):
        subtitles = self.search_by_name(filename, langs)
        if subtitles:
            best_match = subtitles[0]
            maxi = 0
            for subtitle in subtitles:
                ratio = self.compare(filename, subtitle['release'])
                if ratio > maxi:
                    maxi = ratio
                    best_match = subtitle
            return best_match
        return None

    def _query(self, filename, maxnumber, lang, imdbID=None, moviehash=None, bytesize=None):
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
            token = login_result['token']
        except Exception:
            print 'Login Error'
            return subtitles
        results = server.SearchSubtitles(token, [search])
        if results['data']:
            for r in results['data']:
                subtitle = {}
                subtitle['release'] = r['SubFileName']
                subtitle['link'] = r['SubDownloadLink']
                subtitle['lang'] = r['SubLanguageID']
                subtitle['movie'] = r['MovieReleaseName']
                subtitle['date'] = r['SubAddDate']
                subtitles.append(subtitle)
        lang = babelfish.Language.fromalpha2(lang).opensubtitles
        results = [x for x in subtitles if x["lang"] == lang][:maxnumber]
        try:
            server.LogOut(token)
        except:
            print 'Logout Error'
        finally:       
            return results

    def search(self, query, maxnumber, langs):
        results = self._query(query, maxnumber, langs)
        return results