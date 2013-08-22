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
        imdbid = request.POST.getlist("your_IMDB_ID")[0]
        jsonfile = connect_imdb(imdbid)

        mongodb = MongoDBConnection()
        mongodb.insert_collection(jsonfile)
        directors_rating = DirectorsRating(mongodb.collection)
        directors_rating_list = DirectorsRating(mongodb.collection).find()
    return render_to_response("charts/index.html", {'data' : directors_rating_list, "moviedata" : directors_rating.title, "imdbid" : imdbid})

def connect_imdb(imdbid):
        imdbcsv = IMDB_CSV(imdbid)
        return IMDBMovieJson(imdbcsv.csvfilename).convert_csv_to_json()

