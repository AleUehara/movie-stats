# -*- encoding: utf-8 -*-

# Create your views here.
import os
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from core.db.database import *
from core.movieimdb.moviejson import IMDBMovieJson
from core.movieimdb.extract_csv import IMDB_CSV
from settings import ROOT_DIR


def index(request):
    if request.method == 'POST':
        try:
            imdbid = request.POST.getlist("your_IMDB_ID")[0]
            jsonfile = connect_imdb(imdbid)
        except Exception, e:
            return render_to_response("404.html", {'message' : "Data not available for this user"})


        try:
            mongodb = MongoDBConnection()
        except:
            return render_to_response("404.html", {'message' : "Database is out of service"})

        

        mongodb.insert_collection(imdbid, jsonfile)
        
        movie_rate_by_year         = MovieRateByYear(mongodb.collection, imdbid)
        movies_by_year             = MoviesByYear(mongodb.collection, imdbid)
        total_minutes_watched      = TotalMinutesWatched(mongodb.collection, imdbid)
        top_directors_best_rating  = TopDirectorsBestRating(mongodb.collection, imdbid)
        top_directors_watched      = TopDirectorsWatched(mongodb.collection, imdbid)
        movies_by_genres           = MoviesByGenres(mongodb.collection, imdbid)
        top_directors_worse_rating = TopDirectorsWorseRating(mongodb.collection, imdbid)
        #print movies_by_genres.values

        #mongodb.drop_collection()

    return render_to_response("charts/index.html", {'movie_rate_by_year'         : movie_rate_by_year, 
                                                    "movies_by_year"             : movies_by_year, 
                                                    "total_minutes_watched"      : total_minutes_watched,
                                                    "top_directors_best_rating"  : top_directors_best_rating,
                                                    "top_directors_worse_rating" : top_directors_worse_rating,
                                                    "top_directors_watched"      : top_directors_watched,
                                                    "movies_by_genres"           : movies_by_genres,
                                                    "imdbid" : imdbid})

def information(request):
    return render_to_response("emailform.html")

def connect_imdb(imdbid):
        imdbcsv = IMDB_CSV(imdbid)
        return IMDBMovieJson(imdbcsv.csvfilename).convert_csv_to_json()