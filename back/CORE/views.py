import hashlib
import operator
from pathlib import Path
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MovieCollectionListSerializer, SingleMovieCollectionSerializer, SingleTVShowSerializer
from .serializers import TVShowEpisodeSerializer
from .serializers import MovieListSerializer, GenreListSerializer, GenreDetailsSerializer, TVShowListSerializer
from .models import Media, Video, Genre, TVShow
from .utils import Tmdb
import random
from django.db.models import Q
from functools import reduce
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from USER.models import Watchlist, UserProfile
from SYS.utils import add_movie_to_db, add_tv_show_to_db, TMDBAPI


# Create your views here.


class MovieCollectionList(APIView):
    def get(self, request, format=None):
        movies = Media.objects.filter(type='M')
        serializer = MovieCollectionListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieCollectionDetails(APIView):
    def get(self, request, movie_collection_id, format=None):
        try:
            movie_collection = Media.objects.get(tmdb_id=movie_collection_id)
        except Media.DoesNotExist:
            return Response({'error': 'Collection not found'}, status=404)
        serializer = SingleMovieCollectionSerializer(movie_collection, many=False)
        return Response(serializer.data)


@permission_classes([IsAuthenticated])
class MovieDetails(APIView):
    def get(self, request, movie_id, format=None):
        try:
            movie = Video.objects.get(tmdb_id=movie_id)
        except Video.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=404)
        response = serializer = MovieListSerializer(movie, many=False).data
        if Watchlist.objects.filter(user__dj_user=request.user, video__tmdb_id=movie_id):
            response['timestamp'] = Watchlist.objects.get(
                user__dj_user=request.user,
                video__tmdb_id=movie_id
            ).video_timestamp

        response['favourite'] = bool(UserProfile.objects.filter(
            dj_user=request.user,
            movie_wishlist__tmdb_id=movie_id)
        )
        return Response(response)


class GenreList(APIView):
    def get(self, request, format=None):
        genre = Genre.objects.all()
        serializer = GenreListSerializer(genre, many=True)
        return Response(serializer.data)


class GenreDetails(APIView):
    def get(self, request, genre_id, format=None):
        try:
            genre = Genre.objects.get(tmdb_id=genre_id)
        except Genre.DoesNotExist:
            return Response({'error': 'Genre not found'}, status=404)
        serializer = GenreDetailsSerializer(genre, many=False)
        return Response(serializer.data)


class RandomMedia(APIView):
    def get(self, request, filter=None, count=1, format=None):
        movies = []
        tvs = []
        if filter in ['movie', None]:
            movies = Video.objects.filter(type='M')
            movies = list(MovieListSerializer(movies, many=True).data)
            random.shuffle(movies)

        if filter in ['tv', None]:
            tvs = TVShow.objects.filter(type='T')
            tvs = list(SingleTVShowSerializer(tvs, many=True).data)
            random.shuffle(tvs)

        medias = movies + tvs
        if not medias:
            return Response({
                "error": "No results found"
            })

        return Response(medias[:count])


class RandomCollection(APIView):
    def get(self, request, format=None):
        collections = Media.objects.filter(type='M')
        serializer = SingleMovieCollectionSerializer(random.choice(collections), many=False)
        return Response(serializer.data)


class MovieList(APIView):
    def get(self, request, sort_type=None, count=None, format=None):
        movies = Video.objects.filter(type='M')
        if str(sort_type).lower().strip() == 'popular':
            sorted_movies = movies.order_by('-popularity')
        elif str(sort_type).lower().strip() == 'latest':
            sorted_movies = movies.order_by('-release_date')
        elif str(sort_type).lower().strip() == 'top-rated':
            sorted_movies = movies.order_by('-rating')
        elif str(sort_type).lower().strip() == 'newly-added':
            sorted_movies = movies.order_by('-timestamp')
        else:
            sorted_movies = movies.order_by('name')

        serializer = MovieListSerializer(sorted_movies[:count] if count else sorted_movies, many=True)
        return Response(serializer.data)


class Search(APIView):
    def get(self, request, format=None):
        q = request.GET.get('q')
        q_list = q.split(' ')

        search_filters = []
        for key in q_list:
            search_filters.append(Q(name__icontains=key))
            search_filters.append(Q(description__icontains=key))
            if Genre.objects.filter(name__icontains=key):
                search_filters.append(Q(genre=Genre.objects.filter(name__icontains=key).first()))

        movie_query = Video.objects.filter(type='M').filter(reduce(operator.or_, search_filters)).order_by(
            '-popularity')
        tv_query = TVShow.objects.filter(type='T').filter(reduce(operator.or_, search_filters)).order_by('-popularity')
        movies = MovieListSerializer(movie_query, many=True).data
        tvs = TVShowListSerializer(tv_query, many=True).data
        return Response(movies + tvs)


@permission_classes([IsAuthenticated])
class MongoDb(APIView):

    def get(self, request, format=None):
        return Response({'mongoBD': 'mongoDB'})


# ---------------------- TV SHows ----------------------
class TVList(APIView):

    def get(self, request, sort_type=None, count=None, format=None):
        tvs = TVShow.objects.all()
        if str(sort_type).lower().strip() == 'popular':
            sorted_tvs = tvs.order_by('-popularity')
        elif str(sort_type).lower().strip() == 'latest':
            sorted_tvs = tvs.order_by('-release_date')
        elif str(sort_type).lower().strip() == 'top-rated':
            sorted_tvs = tvs.order_by('-rating')
        elif str(sort_type).lower().strip() == 'newly-added':
            sorted_tvs = tvs.order_by('-timestamp')
        else:
            sorted_tvs = tvs.order_by('name')

        serializer = TVShowListSerializer(sorted_tvs[:count] if count else sorted_tvs, many=True)
        return Response(serializer.data)


@permission_classes([IsAuthenticated])
class TVDetails(APIView):
    def get(self, request, tv_id, format=None):
        if not (request.user.is_staff or request.user.is_staff):
            return Response({'error': 'Permission denied !'}, status=403)
        try:
            tvs = TVShow.objects.get(tmdb_id=tv_id)
        except TVShow.DoesNotExist:
            return Response({'error': 'TV Show not found'}, status=404)

        seasons_list = list(tvs.video_set.values_list('season_no', flat=True).distinct())
        seasons = dict()
        for season in seasons_list:
            seasons[int(season)] = TVShowEpisodeSerializer(
                tvs.video_set.filter(season_no=int(season)),
                many=True,
                context={'user': request.user}
            ).data

        serializer = TVShowListSerializer(tvs, many=False)
        response = dict()
        response.update(serializer.data)
        response.update({'seasons': seasons})

        if Watchlist.objects.filter(user__dj_user=request.user, tv__tmdb_id=tv_id):
            response['last_watching'] = Watchlist.objects.get(
                user__dj_user=request.user,
                tv__tmdb_id=tv_id
            ).video.tmdb_id
        response['favourite'] = bool(UserProfile.objects.filter(
            dj_user=request.user,
            tv_wishlist__tmdb_id=tv_id)
        )
        return Response(response)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_tmdb_id(request, data_type: str, tmdb_id):
    new_tmdb_id = request.data.get('new_tmdb_id')
    if data_type.upper() == 'MOVIE':
        if not Video.objects.filter(tmdb_id=tmdb_id):
            return Response({'error': 'No movie found with the tmdb id: {}'.format(tmdb_id)}, status=400)
        movie = Video.objects.get(tmdb_id=tmdb_id)
        tmdbapi = TMDBAPI()
        tmdb_response = tmdbapi.get_movie_by_id(new_tmdb_id)
        video_url = movie.location
        movie.delete()
        add_movie_to_db(tmdb_response, location=video_url)
        return Response(MovieListSerializer(Video.objects.get(tmdb_id=tmdb_response.get('id')), many=False).data)
    elif data_type.upper() == 'TV':
        if not TVShow.objects.filter(tmdb_id=tmdb_id):
            return Response({'error': 'No movie found with the tmdb id: {}'.format(tmdb_id)}, status=400)
        tv = TVShow.objects.get(tmdb_id=tmdb_id)
        tmdbapi = TMDBAPI()
        tmdb_response = tmdbapi.get_tv_show_by_id(new_tmdb_id)
        tv_local_path = tv.local_path
        tv.delete()
        add_tv_show_to_db(
            tmdb_data=tmdb_response,
            location=tv_local_path,
            media_dir_hash=hashlib.md5(str(Path(tv_local_path).parent).encode('utf-8')).hexdigest()
        )
        return Response(TVShowListSerializer(TVShow.objects.get(tmdb_id=tmdb_response.get('id')), many=False).data)
    else:
        return Response({'error': 'Invalid Media Type in url'}, status=400)
