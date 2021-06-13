from django.db import models
import json
from django.db.models import Count


# Create your models here.
class Genre(models.Model):
    tmdb_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    image = models.CharField(max_length=200, blank=True, null=True)

    def get_movies(self):
        return Video.objects.filter(genre__icontains=self.tmdb_id)

    def __str__(self):
        return '[{}, {}]'.format(self.tmdb_id, self.name)


class MediaType:
    MOVIE = 'M'
    TV_SHOWS = 'T'
    UNIDENTIFIED = 'U'

    @staticmethod
    def get_media_type_options():
        return [
            ('M', 'Movie'),
            ('T', 'TV Shows'),
            ('U', 'Unidentified'),
        ]


class Media(models.Model):
    tmdb_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=1, choices=MediaType.get_media_type_options(), default='U')
    is_collection = models.BooleanField(default=False)

    background_image = models.CharField(max_length=500, blank=True, null=True)
    poster_image = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return '{} [{}]'.format(self.name, self.tmdb_id)


class Video(models.Model):  # Movies and Episode
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)
    media = models.ForeignKey(Media, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=200)
    type = models.CharField(max_length=1, choices=MediaType.get_media_type_options(), default='U')
    thumbnail = models.CharField(max_length=500, blank=True, null=True)
    rating = models.FloatField(default=0)
    release_date = models.DateField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    genre = models.ManyToManyField(Genre, blank=True)  # Movie
    logo = models.CharField(max_length=500, blank=True, null=True)  # Movie
    poster_image = models.CharField(max_length=500, blank=True, null=True)  # Movie
    background_image = models.CharField(max_length=500, blank=True, null=True)  # Movie
    popularity = models.FloatField(null=True, blank=True)  # Movie
    tagline = models.CharField(max_length=500, null=True, blank=True)  # Movie
    trailer = models.CharField(max_length=500, blank=True, null=True)  # Movie
    duration = models.DurationField(null=True, blank=True)

    season_no = models.IntegerField(null=True, blank=True)  # TV Shows

    def __str__(self):
        return '{} [{}]'.format(self.name, self.tmdb_id)


class TVShow(Media):
    genre = models.ManyToManyField(Genre, blank=True)
    logo = models.CharField(max_length=200, blank=True, null=True)
    thumbnail = models.CharField(max_length=200, blank=True, null=True)
    popularity = models.FloatField(default=0)
    rating = models.FloatField(default=0)
    release_date = models.DateField(null=True, blank=True)
    episode_runtime = models.DurationField(null=True, blank=True)
    season_count = models.IntegerField(default=1)

    tagline = models.CharField(max_length=500, null=True, blank=True)
    trailer = models.CharField(max_length=500, blank=True, null=True)

    last_watched_episode = models.ForeignKey(Video, null=True, blank=True, on_delete=models.SET_NULL)

    local_path = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return '{} [{}]'.format(self.name, self.tmdb_id)
