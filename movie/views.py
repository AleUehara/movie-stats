# -*- encoding: utf-8 -*-

# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse

def index(resquest):
    #return HttpResponse(u"Ola mundo!")
    return render_to_response("charts/index.html")
