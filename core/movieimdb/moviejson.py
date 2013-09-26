#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import json
import csv

class IMDBMovieJson():
    def __init__(self, filename):
        self.filename = filename
        self.file = open( filename, 'r' )

    def convert_csv_to_json(self):

        header = self.file.readline().replace(".", "")
        reader = csv.DictReader( self.file, fieldnames = ( header.replace("\"", "").split(",") ) )

        movie_list = []
        username = ""

        for row in reader:
           username = self.__find_username(row)

           row["rated"] = int(row[username])
           row["IMDb Rating"] = float(row["IMDb Rating"])
           row["Runtime (mins)"] = 0 if row["Runtime (mins)"] is "" else int(row["Runtime (mins)"])
           movie_list.append(row)


        stringfile = json.dumps( [ row for row in movie_list ] , indent=4)
        movies_json = json.loads(stringfile)

        os.remove(self.filename)
        return movies_json

    def __find_username(self, row):
        for key in row.keys():
          if key.endswith(" rated"):
            return key
        return ""

#----------------------------------------
#Init
#----------------------------------------
if __name__ == "__main__":
    IMDBMovieJson('imdbmovies/temp/movies.csv').convert_csv_to_json()
