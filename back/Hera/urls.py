"""Hera URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings

API_PATH = 'api/v1/'

urlpatterns = []
if settings.DEBUG:
    urlpatterns += [path('admin/', admin.site.urls)]

urlpatterns += [
   # path(API_PATH, include('djoser.urls')),
   # path(API_PATH, include('djoser.urls.authtoken')),

   path(API_PATH, include('CORE.urls')),
   path(API_PATH + 'sys/', include('SYS.urls')),
   path(API_PATH + 'user/', include('USER.urls')),

   url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

for static_dir_hash, static_dir in {**settings.MOVIES_DIRS_MAP, **settings.TVSHOWS_DIRS_MAP}.items():
    urlpatterns + static(settings.MEDIA_URL, document_root=static_dir)
    urlpatterns.append(url(r'^media{id}/(?P<path>.*)$'.format(id=static_dir_hash), serve, {'document_root': static_dir}))
