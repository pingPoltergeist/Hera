import re
import time

import yaml
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
from SYS.models import System, MediaDirectory
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from Hera.apis import TMDB, Fanart
from CORE.models import Video, TVShow, MediaType, Media
from django.contrib.auth.models import User as AuthUser
from django.conf import settings


class Sync(APIView):
    def get(self, request, format=None):
        MediaDirectory.update_media_directory(
            tv_dirs=settings.TVSHOWS_DIRS_MAP,
            movie_dirs=settings.MOVIES_DIRS_MAP
        )

        #  delete removed files
        Video.delete_all_video_with_no_local_file()

        # Delete media with no child
        Media.delete_all_media_with_no_child()

        tmdb = TMDB()
        movies = {}
        for mediaDirectory in MediaDirectory.objects.filter(movie_dir=True):
            non_synced_media_files = mediaDirectory.get_non_synced_movie_files()
            print(mediaDirectory, '=== non_synced_media_files: ', non_synced_media_files)
            for movie_name in non_synced_media_files:
                movie_search_key = re.compile(r'[\w ]*').match(movie_name).group()
                response = tmdb.search_movie(movie_search_key).json()
                if response.get("results"):
                    sync_status = utils.add_movie_to_db(
                        tmdb_data=tmdb.get_movie_by_id(response["results"][0]["id"]),
                        filename=movie_name,
                        media_dir=mediaDirectory
                    )
                    movies[movie_name] = {'status': sync_status, 'tmdb': response["results"][0]["id"]}
            if non_synced_media_files:
                mediaDirectory.movie_last_sync = datetime.datetime.now().astimezone()
                mediaDirectory.save()

        tvs = {}
        for tvDirectory in MediaDirectory.objects.filter(tv_dir=True):
            non_synced_tv_shows: dict = tvDirectory.get_non_synced_tv_shows()
            print(tvDirectory, '=== get_non_synced_tv_shows: ', non_synced_tv_shows)

            for tv_show_name, sub_folders in non_synced_tv_shows.items():
                tv_search_key = re.compile(r'[\w ]*').match(tv_show_name).group()
                response = tmdb.search_tv(tv_search_key).json()
                # print(tv_search_key, response)
                if response.get("results"):
                    sync_status = utils.add_tv_show_to_db(
                        tmdb_data=tmdb.get_tv_show_by_id(response["results"][0]["id"]),
                        tv_files_data={tv_show_name: sub_folders},
                        media_dir=tvDirectory
                    )
                    tvs[tv_show_name] = {'status': sync_status, 'tmdb': response["results"][0]["id"]}
            # if non_synced_tv_shows:
            #     tvDirectory.tv_last_sync = datetime.datetime.now().astimezone()
            #     tvDirectory.save()
        return Response({'movies': movies, 'tvs': tvs})


@api_view(['GET', 'PUT', 'DELETE'])
def handle_media_dirs(request, dir_type=None):
    if request.method == 'GET':
        # print(settings.CONFIG.get())
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
    try:
        with open(settings.BASE_DIR.parent / 'settings.yaml', 'w') as settings_file:
            yaml.dump({'PORT': port}, settings_file)
    except Exception as ex:
        traceback.print_exc()
        return Response({'error': str(ex)}, status=400)
    return Response({'status': True})
