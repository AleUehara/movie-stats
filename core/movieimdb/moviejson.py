#!/usr/bin/python
# -*- encoding: utf-8 -*-
import json
import csv

class IMDBMovies():
    def __init__(self, filename):
        self.file = open( filename, 'r' )

    def convert_csv_to_json(self):

        header = self.file.readline().replace(".", "")
        reader = csv.DictReader( self.file, fieldnames = ( header.replace("\"", "").split(",") ) )

        movie_list = []

        for row in reader:
           row["uehara-alexandre rated"] = int(row["uehara-alexandre rated"])
           row["IMDb Rating"] = float(row["IMDb Rating"])
           #row["Runtime (mins)"] = int(row["Runtime (mins)"])
           row["Runtime (mins)"] = 0 if row["Runtime (mins)"] is "" else int(row["Runtime (mins)"])
           movie_list.append(row)


        stringfile = json.dumps( [ row for row in movie_list ] , indent=4)
        movies_json = json.loads(stringfile)
        return movies_json

#----------------------------------------
#Init
#----------------------------------------
if __name__ == "__main__":
    IMDBMovies('imdbmovies/temp/movies.csv').convert_csv_to_json()
