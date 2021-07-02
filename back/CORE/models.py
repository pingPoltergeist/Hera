import traceback
import os
from datetime import datetime
from pathlib import Path

from django.db import models
from SYS.models import MediaDirectory
from Hera.apis import TMDB, Fanart


# Create your models here.
class Genre(models.Model):
    tmdb_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    image = models.CharField(max_length=200, blank=True, null=True)

    def get_movies(self):
        return Video.objects.filter(genre__icontains=self.tmdb_id)

    def __str__(self):
        return '[{}, {}]'.format(self.tmdb_id, self.name)

    @staticmethod
    def get_or_create_by_genre_obj_list(genre_obj_list):
        if not genre_obj_list:
            return None
        res = dict()
        for genre_obj in genre_obj_list:
            try:
                genre, status = Genre.objects.get_or_create(
                    tmdb_id=genre_obj.get('id'),
                    name=genre_obj.get('name')
                )
                res.update(genre)
            except Exception as e:
                print(e)
        return res


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

    media_dir = models.ForeignKey(MediaDirectory, on_delete=models.CASCADE)

    def __str__(self):
        return '{} [{}]'.format(self.name, self.tmdb_id)

    def delete_if_no_child(self):
        if not self.video_set.all():
            self.delete()
            return True

    @staticmethod
    def delete_all_media_with_no_child():
        count = 0
        for media in Media.objects.all():
            count += 1 if media.delete_if_no_child() else 0
        return count


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

    media_dir = models.ForeignKey(MediaDirectory, on_delete=models.CASCADE)

    def __str__(self):
        return '{} [{}]'.format(self.name, self.tmdb_id)

    def delete_if_file_does_not_exists(self):
        local_path = Path(self.media_dir.folder_location) / '/'.join(self.location.split('/')[2:])
        if not local_path.exists():
            self.delete()
            return True

    @staticmethod
    def delete_all_video_with_no_local_file():
        count = 0
        for video in Video.objects.all():
            count += 1 if video.delete_if_file_does_not_exists() else 0
        return count


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

    def add_episode_from_episode_data(self, episode: dict, location):
        episode_video = None
        try:
            episode_video, status = self.video_set.get_or_create(
                tmdb_id=episode['id'],
                media_dir=self.media_dir
            )

            episode_video.name = episode['name']
            episode_video.description = episode['overview']
            episode_video.rating = episode['vote_average']
            episode_video.season_no = episode['season_number']
            episode_video.type = 'T'
            episode_video.location = location

            if episode['still_path']:
                episode_video.thumbnail = TMDB.TMDB_IMAGE_URL + episode['still_path']
            episode_video.save()
            return True
        except Exception as ex:
            if episode_video:
                episode_video.delete()
            traceback.print_exc()
            return False
