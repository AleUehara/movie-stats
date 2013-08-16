#!/usr/bin/python
# -*- encoding: utf-8 -*-
import json
import csv

f = open( 'temp/movies.csv', 'r' )

header = f.readline()



reader = csv.DictReader( f, fieldnames = ( header.replace("\"", "").split(",") ) )
out = json.dumps( [ row for row in reader ] )

print type(out)


#print out[0]

#for row in reader:
#	print row

#print len(reader)