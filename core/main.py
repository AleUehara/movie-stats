#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
os.path.dirname(os.path.abspath(__file__))
from movieimdb.moviejson import IMDBMovies
from db.database import MongoDBConnection
import ConfigParser
from movieimdb.extract_csv import IMDB_CSV


def main():
    
    #config = ConfigParser.ConfigParser()
    #config.read("movieimdb/imdb.cfg")
    #link_export = "http://www.imdb.com/list/export?list_id=ratings&author_id=ur" + config.get("imdb", "id")
    #IMDB_CSV(link_export).handle()
    




    #jsonfile = IMDBMovies('movieimdb/temp/movies.csv').convert_csv_to_json()
    #print jsonfile
    mongodb = MongoDBConnection()
    #mongodb.insert_collection(jsonfile)
    #mongodb.select_one()
    #mongodb.count()
    #mongodb.all_rates()
    #mongodb.movies_by_directors()
    #mongodb.top_directors_watched(5)
    #mongodb.movies_by_year()
    #mongodb.directors_rating()
    mongodb.movies_rates_by_year()
    #mongodb.total_minutes_watched()


#----------------------------------------
#Init
#----------------------------------------
if __name__ == "__main__":
    main()