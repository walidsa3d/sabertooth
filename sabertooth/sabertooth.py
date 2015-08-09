#!/usr/bin/env python
#walid.saad
import os
import struct
import xmlrpclib
import commands
import gzip
import traceback
import logging
import requests
import shutil
import argparse
from termcolor import colored
import sys
from dateutil.parser import parse


OS_LANGS ={ "en": "eng","fr" : "fre","hu": "hun","cs": "cze","pl" : "pol","sk" : "slo", 
            "pt" : "por","pt-br" : "pob","es" : "spa","el" : "ell","ar":"ara",'sq':'alb',
            "hy":"arm","ay":"ass","bs":"bos","bg":"bul","ca":"cat","zh":"chi","hr":"hrv",
            "da":"dan","nl":"dut","eo":"epo","et":"est","fi":"fin","gl":"glg","ka":"geo",
            "de":"ger","he":"heb","hi":"hin","is":"ice","id":"ind","it":"ita","ja":"jpn",
            "kk":"kaz","ko":"kor","lv":"lav","lt":"lit","lb":"ltz","mk":"mac","ms":"may",
            "no":"nor","oc":"oci","fa":"per","ro":"rum","ru":"rus","sr":"scc","sl":"slv",
            "sv":"swe","th":"tha","tr":"tur","uk":"ukr","vi":"vie"}
class opensubs:
    
    def download_subtitle(self,subtitle):
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

    def query(self,filename, maxnumber, lang,imdbID=None, moviehash=None, bytesize=None):
            #Prepare the search
            search = {}
            sublinks = []
            if moviehash: search['moviehash'] = moviehash
            if imdbID: search['imdbid'] = imdbID
            if bytesize: search['moviebytesize'] = str(bytesize)
            #search['SubLanguageID']="eng,fra,dan"
            # if langs: search['sublanguageid'] = ",".join([self.getLanguage(lang) for lang in langs])
            if len(search) == 0:
                search['query'] = filename              
            #Login
            server = xmlrpclib.Server('http://api.opensubtitles.org/xml-rpc')
            login_result = server.LogIn("","","eng","periscope")
            print login_result
            token = login_result["token"]  
            print token  
            results = server.SearchSubtitles(token, [search])
            sublinks = []
            if results['data']:
                for r in results['data']:
                    result = {}
                    result["release"] = r['SubFileName']
                    result["link"] = r['SubDownloadLink']
                    result["lang"] = r['SubLanguageID']
                    result["movie"]=r['MovieReleaseName']
                    result["date"]=r['SubAddDate']
                    sublinks.append(result)
            lang=OS_LANGS[lang] if lang in OS_LANGS else "eng"
            return [x for x in sublinks if x["lang"]==lang][:maxnumber]        
            try:
                server.LogOut(token)
            except:
                print "Open subtitles could not be contacted for logout"
    def main(self):
        parser = argparse.ArgumentParser(usage="-h for full usage")
        parser.add_argument('query',help='source directory',nargs='+')
        parser.add_argument('-n', dest="maxnumber", help="update database",type=int)
        parser.add_argument('-lang', dest="language", help="update database")
        args = parser.parse_args()
        results=opensubs().query(" ".join(args.query),args.maxnumber,args.language)
        results=dict(enumerate(results))
        for i in results:
            index=colored(i,'red')
            lang=colored(results[i]['lang'],'yellow','on_grey')
            dt=parse(results[i]['date'])
            date=colored(dt.strftime('%d/%m/%Y'),'blue')
            release=colored(results[i]["movie"],'green')
            output="{} {} {} {}".format(index,lang,release,date)
            print output
        choice=raw_input("Choose subtitle to download : \t")
        self.download_subtitle(results[int(choice)])
    
if __name__ == '__main__':
    try:
        opensubs().main()
    except KeyboardInterrupt:
        print "Exiting"
        sys.exit(0)