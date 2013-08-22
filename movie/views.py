# -*- encoding: utf-8 -*-

# Create your views here.
import os
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from core.db.database import MongoDBConnection
from core.movieimdb.moviejson import IMDBMovies
from core.movieimdb.extract_csv import IMDB_CSV
from settings import ROOT_DIR


class MovieData():
	def __init__(self):
		self.nome = "Number"
		self.title = "Top Directors Watched"

def index(request):
    if request.method == 'POST':
        imdb_id = request.POST.getlist("your_IMDB_ID")[0]
        link_export = "http://www.imdb.com/list/export?list_id=ratings&author_id=ur" + imdb_id
        IMDB_CSV(link_export).handle()
        jsonfile = IMDBMovies(os.path.join(ROOT_DIR, "core", "movieimdb", "temp", "movies.csv")).convert_csv_to_json()

        mongodb = MongoDBConnection()
        mongodb.insert_collection(jsonfile)
        data = mongodb.top_directors_watched(5)
        moviedata = MovieData()
    return render_to_response("charts/index.html", {'data' : data, "moviedata" : moviedata, "imdbid" : imdb_id})

