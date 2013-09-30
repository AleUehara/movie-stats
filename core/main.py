#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
os.path.dirname(os.path.abspath(__file__))
from movieimdb.moviejson import IMDBMovieJson
from db.database import *#MongoDBConnection, TopDirectorsRating
import ConfigParser
from movieimdb.extract_csv import IMDB_CSV


def main():
    
    config = ConfigParser.ConfigParser()
    CFG_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "movieimdb", "imdb.cfg")
    config.read(CFG_FILE)
    imdbid = config.get("imdb", "id")
    #imdbcsv = IMDB_CSV(imdbid)

    #print imdbcsv.csvfilename

    
    




    #jsonfile = IMDBMovieJson(imdbcsv.csvfilename).convert_csv_to_json()
    #print jsonfile
    mongodb = MongoDBConnection()
    #mongodb.insert_collection(imdbid, jsonfile)
    #mongodb.select_all()
    #mongodb.select_one()
    #mongodb.count()
    #mongodb.all_rates()
    #mongodb.movies_by_directors()
    #mongodb.top_directors_watched(5)
    #mongodb.movies_by_year()
    #mongodb.directors_rating()
    #mongodb.movies_rates_by_year()
    #mongodb.total_minutes_watched()
    #result = TotalMinutesWatched(mongodb.collection, imdbid)
    #MovieRateByYear(mongodb.collection, imdbid)
    result = MoviesByYear(mongodb.collection, imdbid)
    print result.values
    #result = TopDirectorsRating(mongodb.collection, imdbid)
    result = MoviesByGenres(mongodb.collection, imdbid)
    #TopDirectorsWatched(mongodb.collection, imdbid)
    print result.values


#----------------------------------------
#Init
#----------------------------------------
if __name__ == "__main__":
    main()