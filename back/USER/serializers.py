from rest_framework import serializers
from CORE.models import Video
from .models import Watchlist, UserProfile
from django.contrib.auth.models import User as AuthUser


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            'name', 'description', 'tmdb_id', 'poster_image', 'thumbnail', 'genre', 'popularity', 'timestamp', 'rating',
            'release_date'
        )


class GenreDetailsSerializer(serializers.ModelSerializer):
    movie_list = serializers.SerializerMethodField()

    class Meta:
        model = Watchlist
        fields = (
            'user', 'video', 'duration'
        )

    @staticmethod
    def get_movie_list(obj):
        parts = Video.objects.filter(genre__icontains=obj.tmdb_id).order_by('-popularity')
        return MovieListSerializer(parts, many=True).data


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            'tmdb_id', 'name', 'description', 'genre', 'type', 'poster_image', 'thumbnail'
        )


class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = AuthUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'fullname', 'is_staff', 'is_superuser'
        )

    @staticmethod
    def get_fullname(obj):
        return obj.get_full_name()
