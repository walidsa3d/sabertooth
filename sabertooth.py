import os
import struct
import xmlrpclib
import commands
import gzip
import traceback
import logging
import babelfish


def query(filename, imdbID=None, moviehash=None, bytesize=None, langs=None):
        ''' Makes a query on opensubtitles and returns info about found subtitles.
            Note: if using moviehash, bytesize is required.    '''
        log = logging.getLogger(__name__)
        log.debug('query')
        #Prepare the search
        search = {}
        sublinks = []
        if moviehash: search['moviehash'] = moviehash
        if imdbID: search['imdbid'] = imdbID
        if bytesize: search['moviebytesize'] = str(bytesize)
        search['sublanguageid']="eng"
        # if langs: search['sublanguageid'] = ",".join([self.getLanguage(lang) for lang in langs])
        if len(search) == 0:
            log.debug("No search term, we'll use the filename")
            # Let's try to guess what to search:
            search['query'] = filename
            log.debug(search['query'])
            
        #Login
        server = xmlrpclib.Server('http://api.opensubtitles.org/xml-rpc')
        log_result = server.LogIn("","","eng","periscope")
        log.debug(log_result)
        token = log_result["token"]  
        print token  
        results = server.SearchSubtitles(token, [search])
        sublinks = []
        if results['data']:
            log.debug(results['data'])
            # OpenSubtitles hash function is not robust ... We'll use the MovieReleaseName to help us select the best candidate
            for r in results['data']:
                # Only added if the MovieReleaseName matches the file
                result = {}
                result["release"] = r['SubFileName']
                result["link"] = r['SubDownloadLink']
                sublinks.append(result)
        return sublinks            
         # Search
        print token        # Logout
        try:
            server.LogOut(token)
        except:
            log.error("Open subtitles could not be contacted for logout")
    
 
print query("terminator",imdbID=None, moviehash=None, bytesize=None)