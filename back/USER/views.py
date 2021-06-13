import json
import traceback
from datetime import timedelta, datetime

from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

import CORE.models
import USER.models
from .serializers import MovieListSerializer, WishlistSerializer, UserSerializer
from .models import UserProfile, Watchlist
from CORE.models import Video, TVShow
from django.contrib.auth.models import User as AuthUser


# Create your views here.
@permission_classes([IsAuthenticated])
class Recommendation(APIView):
    def get(self, request, format=None):
        movies = request.user.AuthUser.watchlist_set
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)

        # return JsonResponse({'qq': })


@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST', 'DELETE'])
def watchlist(request, video_id=None):
    userProfile, status = UserProfile.objects.get_or_create(dj_user=request.user)
    if status:
        userProfile.save()
    watchlist_set = userProfile.watchlist_set

    if request.method == 'GET':
        return Response({
            'movies': WishlistSerializer(watchlist_set.filter(video__type=CORE.models.MediaType.MOVIE), many=True).data,
            'tv': WishlistSerializer(watchlist_set.filter(tv__isnull=False), many=True).data
        })

    if request.method == 'POST':
        timestamp = request.data.get('timestamp')
        if not video_id or not timestamp:
            return Response({'error': 'TMDB id / Timestamp missing'}, status=400)

        if Video.objects.filter(tmdb_id=video_id):
            video = Video.objects.get(tmdb_id=video_id)
            wishlist_video, status = watchlist_set.get_or_create(
                user=userProfile,
                video=video
            )
            if timestamp < 0:
                wishlist_video.status = USER.models.WatchStatus.WATCHED
            else:
                wishlist_video.status = USER.models.WatchStatus.WATCHING
                wishlist_video.video_timestamp = timedelta(seconds=timestamp)

            wishlist_video.last_watched = datetime.now()
            if video.type == CORE.models.MediaType.TV_SHOWS:
                wishlist_video.tv = video.media.tvshow
                video.media.tvshow.last_watched_episode = video
                video.media.tvshow.save()

            wishlist_video.save()
        return Response({'status': True})


@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST', 'DELETE'])
def wishlist(request):
    userProfile, status = UserProfile.objects.get_or_create(dj_user=request.user)
    if status:
        userProfile.save()
    if request.method == 'GET':
        tv_list = userProfile.tv_wishlist.all()
        tv_list_serializer = WishlistSerializer(tv_list, many=True)
        movie_list = userProfile.movie_wishlist.filter(type=CORE.models.MediaType.MOVIE)
        movie_list_serializer = WishlistSerializer(movie_list, many=True)
        return Response({
            'movies': movie_list_serializer.data,
            'tvs': tv_list_serializer.data,
        })
    if request.method == 'POST':
        tmdb_id = request.data.get('tmdb_id')
        if not tmdb_id:
            return Response({'error': 'Please send TMDB id'}, status=400)
        if Video.objects.filter(tmdb_id=tmdb_id):
            video = Video.objects.get(tmdb_id=tmdb_id)
            userProfile.movie_wishlist.add(video)
        elif TVShow.objects.filter(tmdb_id=tmdb_id):
            tv = TVShow.objects.get(tmdb_id=tmdb_id)
            userProfile.tv_wishlist.add(tv)
        else:
            return Response({'error': 'invalid TMDB id in adding wishlist'})

    if request.method == 'DELETE':
        tmdb_id = request.data.get('tmdb_id')
        if not tmdb_id:
            return Response({'error': 'Please send TMDB id'}, status=400)
        if Video.objects.filter(tmdb_id=tmdb_id):
            video = Video.objects.get(tmdb_id=tmdb_id)
            userProfile.movie_wishlist.remove(video)
        elif TVShow.objects.filter(tmdb_id=tmdb_id):
            tv = TVShow.objects.get(tmdb_id=tmdb_id)
            userProfile.tv_wishlist.remove(tv)
        else:
            return Response({'error': 'invalid TMDB id in remove wishlist'})

    userProfile.save()
    return Response({'status': True})


@api_view(['GET', 'POST', 'DELETE'])
def user_operations(request):
    data = request.data
    if not (request.user and request.user.is_authenticated):
        return Response({'error': 'Authorization required'}, status=401)
    if not (request.user.is_staff or request.user.is_staff):
        return Response({'error': 'Permission denied !'}, status=403)

    if request.method == 'GET':
        all_users = AuthUser.objects.all()
        return Response(UserSerializer(all_users, many=True).data)
    elif request.method == 'POST':
        if not data.get('username'):
            return Response({'error': 'username is mandatory'}, status=400)
        if not data.get('password'):
            return Response({'error': 'password is mandatory'}, status=400)
        if AuthUser.objects.filter(username=data.get('username')):
            return Response({'error': 'Username already exists !'}, status=400)
        authUser = None
        userprofile = None
        try:
            authUser = AuthUser.objects.create_user(
                username=data.get('username'),
                email=data.get('username'),
                password=data.get('password'),
            )
            authUser.first_name = data.get('firstname') or ''
            authUser.last_name = data.get('lastname') or ''
            userprofile = UserProfile.objects.create(
                dj_user=authUser,
                age=data.get('age') or 18,
            )
            authUser.save()
            userprofile.save()
            return Response({
                'status': 'Success',
                'details': 'User created'
            })
        except Exception as ex:
            if authUser:
                authUser.delete()
            if userprofile:
                userprofile.delete()
            print(ex)
            traceback.print_exc()
            return Response({
                'error': 'Unable to create User !'
            }, status=400)
    elif request.method == 'DELETE':
        if not(data.get('username')):
            return Response({'error': 'username is mandatory'}, status=400)
        if data.get('username') == request.user.username:
            return Response({'error': 'Deleting yourself not allowed'}, status=400)
        try:
            auth_user = AuthUser.objects.get(username=data.get('username'))
            auth_user.delete()
            return Response({'status': 'User Deleted'})
        except Exception as ex:
            traceback.print_exc()
            return Response({'error': str(ex)})
    else:
        return Response({'error': 'Method not allowed'}, status=400)


@permission_classes([IsAuthenticated])
class Profile(APIView):
    def get(self, request, format=None):
        serializer = UserSerializer(request.user, many=False)
        return Response(serializer.data)
