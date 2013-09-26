# -*- encoding: utf-8 -*-

# Create your views here.
import os
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from core.db.database import *#MongoDBConnection, TopDirectorsRating, TotalMinutesWatched, MoviesByYear
from core.movieimdb.moviejson import IMDBMovieJson
from core.movieimdb.extract_csv import IMDB_CSV
from settings import ROOT_DIR


def index(request):
    if request.method == 'POST':
        try:
            imdbid = request.POST.getlist("your_IMDB_ID")[0]
            jsonfile = connect_imdb(imdbid)
        except Exception, e:
            #print "---------------------"
            #print e
            return render_to_response("404.html", {'message' : "Data not available for this user"})


        try:
            mongodb = MongoDBConnection()
        except:
            return render_to_response("404.html", {'message' : "Database is out of service"})

        

        mongodb.insert_collection(imdbid, jsonfile)
        
        #directors_rating = TopDirectorsRating(mongodb.collection)
        movie_rate_by_year = MovieRateByYear(mongodb.collection, imdbid)
        movies_by_year   = MoviesByYear(mongodb.collection, imdbid)

        #mongodb.drop_collection()

    #return render_to_response("charts/index.html", {'directors_rating' : directors_rating, "movies_by_year" : movies_by_year, "imdbid" : imdbid})
    return render_to_response("charts/index.html", {'movie_rate_by_year' : movie_rate_by_year, "movies_by_year" : movies_by_year, "imdbid" : imdbid})

def connect_imdb(imdbid):
        imdbcsv = IMDB_CSV(imdbid)
        return IMDBMovieJson(imdbcsv.csvfilename).convert_csv_to_json()

#libapache2-mod-wsgi