from enum import Enum
from django.contrib.auth.models import User as AuthUser
from django.db import models
from CORE.models import Video, TVShow


# Create your models here.
class WatchStatus:
    UNWATCHED = 0
    WATCHING = 1
    WATCHED = 2

    @staticmethod
    def get_all_watch_status():
        return [
            ('0', 'UNWATCHED'),
            ('1', 'WATCHING'),
            ('2', 'WATCHED')
        ]


class UserProfile(models.Model):
    dj_user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name='UserProfile')
    search_history = models.CharField(max_length=250, blank=True, null=True)
    age = models.IntegerField(default=18)
    chosen_genres = models.CharField(max_length=70, blank=True, null=True)
    movie_wishlist = models.ManyToManyField(Video, blank=True)
    tv_wishlist = models.ManyToManyField(TVShow, blank=True)

    def __str__(self):
        return '{}'.format(self.dj_user.username)


class Watchlist(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    tv = models.ForeignKey(TVShow, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(choices=WatchStatus.get_all_watch_status(), max_length=2, default=0)
    video_timestamp = models.DurationField(null=True, blank=True)
    last_watched = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.user.dj_user.username, self.video.tmdb_id)
