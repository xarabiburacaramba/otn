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
    c=[]
    cursor.execute("select name from map_compositions")
    for rec in cursor:
      c.append(rec[0])
    return JsonResponse(c, safe=False) 
    cursor.close()