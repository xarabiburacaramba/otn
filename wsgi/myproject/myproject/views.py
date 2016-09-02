from django.conf.urls import url
from django import forms
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.exceptions import ValidationError
from django.http import StreamingHttpResponse
from django.http import JsonResponse
from django.shortcuts import render

import os
import sys
import psycopg2
import mimetypes
import json


def index(request):
  return HttpResponse('Hello World')
  
connection=psycopg2.connect("dbname=otn user=adminphaewqf password=dSeAnnfTss-R host=127.7.14.2 port=5432")

def get_compositions(request):
    cursor=connection.cursor()
    cursor.execute("select array_to_json(array_agg(map_compositions)) from map_compositions")
    c=cursor.fetchone()[0]
    return JsonResponse(c, safe=False) 
    cursor.close()
    
    
def find_museum(request, route_id):
    cursor=connection.cursor()
    cursor.execute("SELECT array_to_json(array_agg(t)) FROM (select a.*, b.layer_order from map_layers a, compositions_layers b where a.layer_id=b.layer_id and b.composition_id='%s' order by layer_order asc) t" %composition_id)
    d=cursor.fetchone()[0]
    return JsonResponse(d, safe=False) 
    cursor.close()