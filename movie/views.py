# -*- encoding: utf-8 -*-

# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from core.db.database import MongoDBConnection

class MovieData():
	def __init__(self):
		self.nome = "Number"
		self.title = "Top Directors Watched"

def index(resquest):
    mongodb = MongoDBConnection()
    data = mongodb.top_directors_watched(5)
    moviedata = MovieData()
    return render_to_response("charts/index.html", {'data' : data, "moviedata" : moviedata})
