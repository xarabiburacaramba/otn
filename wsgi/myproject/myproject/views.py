from django.conf.urls import url
from django import forms
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.exceptions import ValidationError
#from django.http import StreamingHttpResponse
from django.core.servers.basehttp import FileWrapper
from django.http import JsonResponse
from django.shortcuts import render

import os
import io
import sys
import logging
import psycopg2
import mimetypes
import json
import zipfile

import myproject.settings


def index(request):
  return HttpResponse(' ')
  
connection=psycopg2.connect("dbname=otn user=adminphaewqf password=dSeAnnfTss-R host=127.7.14.2 port=5432")


def get_roadworks(request):
    cursor=connection.cursor()
    cursor.execute("select array_to_json(array_agg(t)) from (select id,name,location,description,detour,array_date_string_format(dates,'DD.MM.YYYY') as dates,geom_json as geom from roadworks) t")
    c=cursor.fetchone()[0]
    return JsonResponse(c, safe=False) 
    cursor.close()

      
      
def get_compositions(request):
    if request.GET.get('language')=='cs':
      cursor=connection.cursor()
      cursor.execute("select array_to_json(array_agg(t)) from (select composition_id, name__cz as name, description__cz as description, custom_attributes__cz as custom_attributes from map_compositions) t")
      c=cursor.fetchone()[0]
      return JsonResponse(c, safe=False) 
      cursor.close()
    else:
      cursor=connection.cursor()
      cursor.execute("select array_to_json(array_agg(t)) from (select composition_id, name, description, custom_attributes from map_compositions) t")
      c=cursor.fetchone()[0]
      return JsonResponse(c, safe=False) 
      cursor.close()
    
    
def get_layers(request, composition_id):
    if request.GET.get('language')=='cs':
      cursor=connection.cursor()
      cursor.execute("SELECT array_to_json(array_agg(t)) FROM (select a.*, b.layer_order from (select layer_id, name__cz as name, description__cz as description, wms_url__cz as wms_url, wms_layer_name__cz as wms_layer_name, custom_attributes__cz as custom_attributes from map_layers) a, compositions_layers b where a.layer_id=b.layer_id and b.composition_id='%s' order by layer_order asc) t" %composition_id)
      d=cursor.fetchone()[0]
      return JsonResponse(d, safe=False) 
      cursor.close()
    else:
      cursor=connection.cursor()
      cursor.execute("SELECT array_to_json(array_agg(t)) FROM (select a.*, b.layer_order from (select layer_id, name, description, wms_url, wms_layer_name, custom_attributes from map_layers) a, compositions_layers b where a.layer_id=b.layer_id and b.composition_id='%s' order by layer_order asc) t" %composition_id)
      d=cursor.fetchone()[0]
      return JsonResponse(d, safe=False) 
      cursor.close()
           
def get_news(request, time_period):
    if request.GET.get('language')=='cs':
      cursor=connection.cursor()
      cursor.execute("SELECT array_to_json(array_agg(t)) FROM (SELECT news_id, category, the_time, geom_json as geom, title__cz as title, content__cz as content, custom_attributes__cz as custom_attributes from news where the_time between (now() - interval '%s hours') and now() order by the_time desc) t" %time_period)
      e=cursor.fetchone()[0]
      return JsonResponse(e, safe=False) 
      cursor.close()
    else:
      cursor=connection.cursor()
      cursor.execute("SELECT array_to_json(array_agg(t)) FROM (SELECT news_id, category, the_time, geom_json as geom, title, content, custom_attributes from news where the_time between (now() - interval '%s hours') and now() order by the_time desc) t" %time_period)
      e=cursor.fetchone()[0]
      return JsonResponse(e, safe=False) 
      cursor.close()
    
def get_all_news(request):
    if request.GET.get('language')=='cs':
      cursor=connection.cursor()
      cursor.execute("SELECT array_to_json(array_agg(t)) FROM (SELECT news_id, category, the_time, geom_json as geom, title__cz as title, content__cz as content, custom_attributes__cz as custom_attributes from news order by the_time desc) t")
      f=cursor.fetchone()[0]
      return JsonResponse(f, safe=False) 
      cursor.close()
    else:
      cursor=connection.cursor()
      cursor.execute("SELECT array_to_json(array_agg(t)) FROM (SELECT news_id, category, the_time, geom_json as geom, title, content, custom_attributes from news order by the_time desc) t")
      f=cursor.fetchone()[0]
      return JsonResponse(f, safe=False) 
      cursor.close()
    
def get_folder_date(request):
    folder_path = os.path.join(myproject.settings.STATIC_ROOT, 'helpapp')
    time_modified = {'time':('%s' % os.path.getmtime(folder_path) )}
    return JsonResponse(time_modified, safe=False)
    
def get_folder_date__cz(request):
    folder_path = os.path.join(myproject.settings.STATIC_ROOT, 'helpapp_cz')
    time_modified = {'time':('%s' % os.path.getmtime(folder_path) )}
    return JsonResponse(time_modified, safe=False)
    
def get_folder_content(request):  
    response = HttpResponse(zip_paths(os.path.join(myproject.settings.STATIC_ROOT, 'helpapp')).getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename={}'.format("%s" % ('content.zip'))
    return response

def get_folder_content__cz(request):  
    response = HttpResponse(zip_paths(os.path.join(myproject.settings.STATIC_ROOT, 'helpapp_cz')).getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename={}'.format("%s" % ('content.zip'))
    return response
           
def zip_paths(paths):
    """
    Compresses directories and files to a single zip file.
    
    Returns the zip file as a data stream, None if error.
    """
    # Check single path vs. multiple
    if isinstance(paths, str):
        paths = (paths,)

    # Filter out non-existent paths
    paths = [x for x in paths if os.path.exists(x)]

    # Make sure the zip file will actually contain something
    if not paths:
        logging.warning("No files/folders to add, not creating zip file")
        return None

    logging.debug("Creating zip file")
    zip_stream = io.BytesIO()
    try:
        zfile = zipfile.ZipFile(zip_stream, 'w', compression=zipfile.ZIP_DEFLATED)
    except EnvironmentError as e:
        logging.warning("Couldn't create zip file")
        return None

    for path in paths:
        if os.path.isdir(path):
            root_len = len(os.path.abspath(path))

            # If compressing multiple things, preserve the top-level folder names
            if len(paths) > 1:
                root_len -= len(os.path.basename(path)) + len(os.sep)

            # Walk through the directory, adding all files
            for root, dirs, files in os.walk(path):
                archive_root = os.path.abspath(root)[root_len:]
                for f in files:
                    fullpath = os.path.join(root, f)
                    archive_name = os.path.join(archive_root, f)
                    try:
                        zfile.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
                    except EnvironmentError as e:
                        logging.warning("Couldn't add file: %s", (str(e),))
        else:
            # Exists and not a directory, assume a file
            try:
                zfile.write(path, os.path.basename(path), zipfile.ZIP_DEFLATED)
            except EnvironmentError as e:
                logging.warning("Couldn't add file: %s", (str(e),))
    zfile.close()
    zip_stream.seek(0)

    return zip_stream