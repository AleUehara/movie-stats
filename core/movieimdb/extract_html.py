#!/usr/bin/python
# -*- coding: utf-8 -*-

import mechanize
import cookielib
import re

class IMDB_API():
    def __init__(self):
        self.mech = mechanize.Browser()

        self.mech.set_handle_robots(False)

        self.cj = cookielib.LWPCookieJar()
        self.mech.set_cookiejar(self.cj)

        # Browser options
        self.mech.set_handle_equiv(True)
        #br.set_handle_gzip(True)
        self.mech.set_handle_redirect(True)
        self.mech.set_handle_referer(True)
        self.mech.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        #self.mech.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # Want debugging messages?
        #self.mech.set_debug_http(True)
        #self.mech.set_debug_redirects(True)
        #self.mech.set_debug_responses(True)

        # User-Agent (this is cheating, ok?)
        self.mech.addheaders = [
        ("Connection", "keep-alive"),
        ('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4'),
        ('x-api-key', 'ITY5wXJ3zSjV2PfdatrEyFjOFPOmpDsJH82J/c+zAmthxY3qcFnb1Q=='),
        ]

    def download(self, link):
    	self.__download_html(link)

    def __download_html(self, link):
        returnvalue = self.mech.open(link)
        htmlfile = open("imdb.html", 'w')
        htmlfile.write(self.mech.response().read())
        htmlfile.close()

class IMDB_HTML():
    def __init__(self, link):
        IMDB_API().download(link)

    def handle(self):
        text = open("imdb.html", 'r')
        m = re.findall(r'\/tt.*', text.read())
        for movie_id in m:
            print movie_id[0:11]
        text.close()

#----------------------------------------
#Init
#----------------------------------------
if __name__ == "__main__":
    link = "http://www.imdb.com/user/ur"+"/ratings"
    IMDB_HTML(link).handle()

