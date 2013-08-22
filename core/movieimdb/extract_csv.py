#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import csv
import urllib2
import ConfigParser
from imdb import IMDb
from settings import ROOT_DIR

CONFIG = ConfigParser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), "imdb.cfg"))
#ROOT_DIR="/home/alexandre/scripts/moviestats"



class IMDB_Site():
    def __init__(self, imdbid):
        self.imdbid      = imdbid

    def download_csv(self, link, csvfilename):
        response = urllib2.urlopen(link)
        movie_data = response.read()

        filename = open(csvfilename, 'w')
        filename.write(movie_data)
        filename.close()




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
        #reader = csv.reader(open(self.imdb.file_movies, "r"), dialect='excel')
        #IMDB_File().create_file(reader)
        pass

'''
class IMDB_File():
    def __init__(self):
        self.filename = os.path.join(ROOT_DIR, "core", "movieimdb", "temp", "movies.temp")

    def create_file(self, reader):
        filename = open(self.filename, 'w')
        ia = IMDb()

        isheader = True
        for row in reader:

            if isheader:
                isheader = False
                continue

            movie_id = int(row[1][2:])
            #print movie_id

            #self.call_python_api(movie_id, filename, row)
            #self.call_imdbapi(movie_id, filename)

        filename.close()

    def call_python_api(self, movie_id, filename, row):
        ia = IMDb()
        movie = ia.get_movie(movie_id)

        #print movie
        
        #for actor in movie['cast']:
        #    print actor
        #    print actor.personID
        
        row.append(movie['cast'])
        print movie['cast']
        filename.write(str(row) + "\n")

    def call_imdbapi(self, movie_id, filename):
        print movie_id

        #movie_id = raw_input('Enter the ID of the movie: ')
        json = urllib2.urlopen('http://imdbapi.com/?i=' + str(movie_id) + '&r=json')

        print json.read()
'''

#----------------------------------------
#Init
#----------------------------------------
if __name__ == "__main__":
    config = ConfigParser.ConfigParser()
    config.read("imdb.cfg")
    imdbid = config.get("imdb", "id")
    #link_export = "http://www.imdb.com/list/export?list_id=ratings&author_id=ur" + imdbid
    #IMDB_CSV(imdbid).handle()
    IMDB_CSV(imdbid)
