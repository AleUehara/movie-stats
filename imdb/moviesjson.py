#!/usr/bin/python
# -*- encoding: utf-8 -*-
import json
import csv

f = open( 'temp/movies.csv', 'r' )

header = f.readline()



reader = csv.DictReader( f, fieldnames = ( header.replace("\"", "").split(",") ) )
stringfile = json.dumps( [ row for row in reader ] , indent=4)
movies_json = json.loads(stringfile)

#print len(jsonfile)

for movie in movies_json:
    print movie.get("Directors")

