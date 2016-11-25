"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import myproject.views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', myproject.views.index),
    url(r'^get_compositions/$', myproject.views.get_compositions, name='get_compositions'),
    url(r'^get_layers/(?P<composition_id>[0-9]+)/$', myproject.views.get_layers, name='get_layers'),
    url(r'^get_news/(?P<time_period>[0-9]+(\.[0-9][0-9]?)?)/$', myproject.views.get_news, name='get_news'),
    url(r'^get_news/$', myproject.views.get_all_news, name='get_all_news'),
    url(r'^get_content_date/$', myproject.views.get_folder_date, name='get_folder_date'),
    url(r'^get_content_date/cz/$', myproject.views.get_folder_date__cz, name='get_folder_date__cz'),
    url(r'^get_content/$', myproject.views.get_folder_content, name='get_folder_content'),
    url(r'^get_content/cz/$', myproject.views.get_folder_content__cz, name='get_folder_content__cz'),
]