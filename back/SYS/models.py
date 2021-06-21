from django.db import models


# Create your models here.

class System(models.Model):
    key = models.CharField(primary_key=True, max_length=1000)
    value = models.CharField(max_length=1000, blank=True, null=True)


class MediaDirectoryType:
    MOVIE = 'M'
    TV_SHOWS = 'T'
    SELECT_ONE = 'S'

    @staticmethod
    def get_media_type_options():
        return [
            ('M', 'Movie'),
            ('T', 'TV Shows'),
            ('S', 'Select One'),
        ]


class MediaDirectory(models.Model):
    folder_location = models.CharField(max_length=1000)
    folder_hash = models.CharField(max_length=100, unique=True)
    last_sync = models.DateTimeField(null=True, blank=True)
    folder_type = models.CharField(
        max_length=1, choices=MediaDirectoryType.get_media_type_options(), default=MediaDirectoryType.SELECT_ONE
    )
