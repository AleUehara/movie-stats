#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
os.path.dirname(os.path.abspath(__file__))
from imdb.moviejson import IMDBMovies
from db.database import MongoDBConnection

def main():
    #jsonfile = IMDBMovies('imdb/temp/movies.csv').convert_csv_to_json()
    #print jsonfile
    mongodb = MongoDBConnection()
    #mongodb.insert_collection(jsonfile)
    mongodb.select_one()
    mongodb.count()
    mongodb.all_rates()


#----------------------------------------
#Init
#----------------------------------------
if __name__ == "__main__":
    main()