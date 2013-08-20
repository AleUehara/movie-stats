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
        stringfile = json.dumps( [ row for row in reader ] , indent=4)
        movies_json = json.loads(stringfile)

        return movies_json

        #print len(jsonfile)

        #for movie in movies_json:
        #    print movie.get("Directors")

#----------------------------------------
#Init
#----------------------------------------
if __name__ == "__main__":
    IMDBMovies('temp/movies.csv').convert_csv_to_json()