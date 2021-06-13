import json
import re
import socket
import traceback
import datetime
from django.db.models import Sum
from rest_framework.decorators import api_view

import CORE.models
from Hera import settings
from pathlib import Path
from rest_framework.response import Response
from rest_framework.views import APIView
from . import utils

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes

from CORE.models import Video, TVShow
from django.contrib.auth.models import User as AuthUser
from django.conf import settings


class Sync(APIView):
    def get(self, request, format=None):
        tmdbapi = utils.TMDBAPI()
        movies = utils.get_all_movie_file_stat()
        for movie_name, details in movies.items():
            movie_search_key = re.compile('[\w ]*').match(movie_name).group()
            response = tmdbapi.search_movie(movie_search_key).json()
            if response.get("results"):
                movies[movie_name]['tmdb_id'] = response["results"][0]["id"]
                movies[movie_name]['title'] = response["results"][0]["original_title"]
                sync_status = utils.add_movie_to_db(
                    tmdbapi.get_movie_by_id(response["results"][0]["id"]),
                    '/media{id}/{filename}'.format(id=details.get('media_dir_hash'), filename=movie_name)
                )
                movies[movie_name]['sync_status'] = sync_status

        tvs = utils.get_all_tv_show_file_stat()
        for tv_show_name, details in tvs.items():
            tv_search_key = re.compile('[\w ]*').match(tv_show_name).group()
            response = tmdbapi.search_tv(tv_search_key).json()
            # print(tv_search_key, response)
            if response.get("results"):
                sync_status = utils.add_tv_show_to_db(tmdbapi.get_tv_show_by_id(
                    response["results"][0]["id"]),
                    details.get('location'),
                    details.get('media_dir_hash')
                )
                tvs[tv_show_name].update({
                    'tmdb_id': response["results"][0]["id"],
                    'name': response["results"][0]["name"],
                    'sync_status': sync_status
                })

        return Response({'movies': movies, 'tvs': tvs})


@api_view(['GET', 'PUT', 'DELETE'])
def handle_media_dirs(request, dir_type=None):
    if request.method == 'GET':
        print(settings.CONFIG.get())
        return Response(settings.CONFIG.get())

    # For updating the dir records
    if request.method == 'PUT':
        body = request.data
        if (not body.get('dir')) and (type(body.get('dir')) != str):
            return Response({'error': "Not a valid data, Please send a str in 'dir' key"}, 500)

        body['dir'] = body.get('dir').strip()

        if not Path(body.get('dir')).is_dir():
            return Response({'error': "Directory doesn't exists"}, 400)

        if (not dir_type) or dir_type.upper() == 'MOVIE':
            settings.CONFIG.add_to_movie_dirs(body.get('dir'))
        if (not dir_type) or dir_type.upper() == 'TV':
            settings.CONFIG.add_to_tv_dirs(body.get('dir'))
        settings.CONFIG.update()
        return Response(settings.CONFIG.get())

    if request.method == 'DELETE':
        body = request.data
        if (not body.get('dir')) and (type(body.get('dir')) != str):
            return Response({'error': "Not a valid data, Please send a str in 'dir' key"}, 500)

        body['dir'] = body.get('dir').strip()

        if (not dir_type) or dir_type.upper() == 'MOVIE':
            if body.get('dir') in settings.CONFIG.get().get('movie_dir'):
                settings.CONFIG.get().get('movie_dir').remove(body.get('dir'))

        if (not dir_type) or dir_type.upper() == 'TV':
            if body.get('dir') in settings.CONFIG.get().get('tv_dir'):
                settings.CONFIG.get().get('tv_dir').remove(body.get('dir'))

        settings.CONFIG.update()
        return Response(settings.CONFIG.get())


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_count(request, count_type: str = None):
    if not request.user.is_superuser or not request.user.is_staff:
        return Response({'error': 'Permission Denied !'}, status=403)
    if count_type.upper() == 'MOVIE':
        return Response({
            'count': Video.objects.filter(type=CORE.models.MediaType.MOVIE).count()
        })
    elif count_type.upper() == 'TV':
        return Response({
            'count': TVShow.objects.all().count()
        })
    elif count_type.upper() == 'USER':
        return Response({
            'count': AuthUser.objects.all().count()
        })
    else:
        return Response({'error': 'Invalid type'}, status=400)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_duration(request):
    if not request.user.is_superuser or not request.user.is_staff:
        return Response({'error': 'Permission Denied !'}, status=403)

    total_movie_duration = Video.objects.filter(
        type=CORE.models.MediaType.MOVIE
    ).aggregate(
        Sum('duration')
    ).get('duration__sum') or datetime.timedelta(minutes=0)

    total_tv_duration = Video.objects.filter(
        type=CORE.models.MediaType.TV_SHOWS
    ).aggregate(
        Sum('media__tvshow__episode_runtime')
    ).get('media__tvshow__episode_runtime__sum') or datetime.timedelta(minutes=0)
    total_duration = total_movie_duration + total_tv_duration

    return Response({
        'total': {
            'days': total_duration.days,
            'Hour': total_duration.seconds // 3600 if total_duration else 0,
            'Min': (total_duration.seconds % 3600) // 60 if total_duration else 0,
        },
        'movie': {
            'days': total_movie_duration.days,
            'Hour': total_movie_duration.seconds // 3600 if total_movie_duration else 0,
            'Min': (total_movie_duration.seconds % 3600) // 60 if total_movie_duration else 0,
        },
        'tv': {
            'days': total_tv_duration.days,
            'Hour': total_tv_duration.seconds // 3600 if total_tv_duration else 0,
            'Min': (total_tv_duration.seconds % 3600) // 60 if total_tv_duration else 0,
        }
    })


@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def update_port(request):
    if not request.user.is_superuser or not request.user.is_staff:
        return Response({'error': 'Permission Denied !'}, status=403)
    port = int(request.data.get('port')) if request.data.get('port') else None
    if not type(port) == int:
        return Response({'error': 'port is mandatory integer field'}, status=400)
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    API = 'API={local_ip}:{port}/api/v1'.format(local_ip=local_ip, port=port)
    BACKEND = 'BACKEND={local_ip}:{port}'.format(local_ip=local_ip, port=port)
    try:
        with open(settings.BASE_DIR.parent / 'front/.env', 'w') as env:
            content = API + '\n' + BACKEND
            env.write(content)
        with open(settings.BASE_DIR / '.env', 'w') as env:
            env.write('PORT={port}'.format(port=port + 1))
    except Exception as ex:
        traceback.print_exc()
        return Response({'error': str(ex)}, status=400)
    return Response({'status': True})
