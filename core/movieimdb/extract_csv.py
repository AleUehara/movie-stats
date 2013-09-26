#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import csv
import urllib2
import ConfigParser
from imdb import IMDb
try:
    from settings import ROOT_DIR
except:
    ROOT_DIR=os.path.realpath(__file__)

CONFIG = ConfigParser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), "imdb.cfg"))
#ROOT_DIR="/home/alexandre/scripts/moviestats"



class IMDB_Site():
    def __init__(self, imdbid):
        self.imdbid      = imdbid

    def download_csv(self, link, csvfilename):
        try:
            response = urllib2.urlopen(link)
            movie_data = response.read()

            filename = open(csvfilename, 'w')
            filename.write(movie_data)
            filename.close()
        except:
            raise Exception("erro")




class IMDB_CSV():
    def __init__(self, imdbid):
        self.imdb = IMDB_Site(imdbid)
        self.link = self.find_imdb_link_csv(imdbid)
        self.csvfilename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temp", imdbid + CONFIG.get("imdb", "csv_sufix_name"))
        self.imdb.download_csv(self.link, self.csvfilename)

    def find_imdb_link_csv(self, imdbid):
        imdblink = CONFIG.get("imdb", "link")
        return imdblink + imdbid

    def handle(self):
        pass


#----------------------------------------
#Init
#----------------------------------------
if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read("imdb.cfg")
    imdbid = config.get("imdb", "id")
    IMDB_CSV(imdbid)
