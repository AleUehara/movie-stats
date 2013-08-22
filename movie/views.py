# -*- encoding: utf-8 -*-

# Create your views here.
import os
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from core.db.database import MongoDBConnection, DirectorsRating
from core.movieimdb.moviejson import IMDBMovieJson
from core.movieimdb.extract_csv import IMDB_CSV
from settings import ROOT_DIR


def index(request):
    if request.method == 'POST':
        try:
            imdbid = request.POST.getlist("your_IMDB_ID")[0]
            jsonfile = connect_imdb(imdbid)
        except:
            render_to_response("404.html")


        mongodb = MongoDBConnection()
        mongodb.insert_collection(jsonfile)
        
        directors_rating = DirectorsRating(mongodb.collection)

        mongodb.drop_collection()

    return render_to_response("charts/index.html", {'directors_rating' : directors_rating, "imdbid" : imdbid})

def connect_imdb(imdbid):
        imdbcsv = IMDB_CSV(imdbid)
        return IMDBMovieJson(imdbcsv.csvfilename).convert_csv_to_json()

