from rest_framework import serializers

from .models import Media, Video, Genre, TVShow
from USER.models import Watchlist, UserProfile


class MovieCollectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = (
            'name', 'tmdb_id', 'poster_image'
        )


class MovieCollectionPartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            'name', 'tmdb_id', 'poster_image', 'location'
        )


class SingleMovieCollectionSerializer(serializers.ModelSerializer):
    parts = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = (
            'name', 'description', 'tmdb_id', 'background_image', 'poster_image', 'parts', 'background_image'
        )

    def get_parts(self, obj):
        parts = obj.video_set.all().order_by('release_date')  # Video.objects.filter(list=obj)
        return MovieCollectionPartsSerializer(parts, many=True).data


class MovieDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            'name', 'description', 'tmdb_id', 'background_image', 'logo', 'genre', 'location'
        )


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'tmdb_id', 'name'
        )


# ------------------------- new -------------------------
class TVShowEpisodeSerializer(serializers.ModelSerializer):
    timestamp = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = (
            'name', 'description', 'tmdb_id', 'poster_image', 'thumbnail', 'popularity', 'rating',
            'release_date', 'logo', 'background_image', 'location', 'timestamp'
        )

    def get_timestamp(self, obj):
        user = self.context.get('user')
        if Watchlist.objects.filter(video__tmdb_id=obj.tmdb_id, user__dj_user=user):
            return Watchlist.objects.get(video__tmdb_id=obj.tmdb_id, user__dj_user=user).video_timestamp


class TVShowListSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()

    class Meta:
        model = TVShow
        fields = (
            'name', 'description', 'tmdb_id', 'poster_image', 'thumbnail', 'genres', 'popularity', 'rating',
            'release_date', 'logo', 'background_image', 'tagline', 'trailer', 'episode_runtime', 'type'
        )

    @staticmethod
    def get_genres(obj):
        genre_list = obj.genre.all()
        return GenreSerializer(genre_list, many=True).data


class MovieListSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()
    favourite = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = (
            'name', 'description', 'tmdb_id', 'poster_image', 'thumbnail', 'genres', 'popularity', 'rating',
            'release_date', 'logo', 'background_image', 'tagline', 'trailer', 'duration', 'location', 'type',
            'timestamp', 'favourite'
        )

    @staticmethod
    def get_genres(obj):
        genre_list = obj.genre.all()
        return GenreSerializer(genre_list, many=True).data

    def get_timestamp(self, obj):
        user = self.context.get('user')
        if Watchlist.objects.filter(user__dj_user=user, video__tmdb_id=obj.tmdb_id):
            return Watchlist.objects.get(
                user__dj_user=user,
                video__tmdb_id=obj.tmdb_id
            ).video_timestamp
        print(user, obj)

    def get_favourite(self, obj):
        user = self.context.get('user')
        return bool(UserProfile.objects.filter(
            dj_user=user,
            movie_wishlist__tmdb_id=obj.tmdb_id)
        )


class SingleTVShowSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    seasons = serializers.SerializerMethodField()
    last_watch = serializers.SerializerMethodField()

    class Meta:
        model = TVShow
        fields = (
            'name', 'description', 'tmdb_id', 'logo', 'background_image', 'genres',
            'season_count', 'rating', 'poster_image', 'thumbnail', 'seasons', 'last_watch',
        )

    @staticmethod
    def get_genres(obj):
        genre_list = obj.genre.all()
        return GenreSerializer(genre_list, many=True).data

    @staticmethod
    def get_seasons(obj):
        seasons_list = list(obj.video_set.values_list('season_no', flat=True).distinct())
        seasons = dict()
        for season in seasons_list:
            seasons[int(season)] = TVShowEpisodeSerializer(obj.video_set.filter(season_no=int(season)), many=True).data
        return seasons

    def get_last_watch(self, obj):
        user = self.context.get("user")
        if Watchlist.objects.filter(user__dj_user=user, tv__tmdb_id=obj.tmdb_id):
            last_watching = Watchlist.objects.get(
                user__dj_user=user,
                tv__tmdb_id=obj.tmdb_id
            ).video
            return {
                'season_no': last_watching.season_no,
                'episode_tmdb_id': last_watching.tmdb_id
            }
        else:
            return None


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'tmdb_id', 'name'
        )


class GenreMovieSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = (
            'name', 'description', 'tmdb_id', 'poster_image', 'thumbnail', 'genres', 'rating'
        )

    @staticmethod
    def get_genres(obj):
        genre_list = obj.genre.all()
        return GenreSerializer(genre_list, many=True).data


class GenreTVShowSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()

    class Meta:
        model = TVShow
        fields = (
            'name', 'description', 'tmdb_id', 'poster_image', 'thumbnail', 'genres', 'season_count', 'rating'
        )

    @staticmethod
    def get_genres(obj):
        genre_list = obj.genre.all()
        return GenreSerializer(genre_list, many=True).data


class GenreDetailsSerializer(serializers.ModelSerializer):
    movies = serializers.SerializerMethodField()
    tv_shows = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = (
            'tmdb_id', 'name', 'movies', 'tv_shows'
        )

    @staticmethod
    def get_movies(obj):
        movies_list = obj.video_set.filter(type='M').order_by('-popularity')
        return GenreMovieSerializer(movies_list, many=True).data

    @staticmethod
    def get_tv_shows(obj):
        tv_show_list = obj.tvshow_set.all().order_by('-popularity')
        return GenreTVShowSerializer(tv_show_list, many=True).data
