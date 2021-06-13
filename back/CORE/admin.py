from django.contrib import admin
from .models import Media, Video, Genre, TVShow


# Register your models here.
class MediaAdmin(admin.ModelAdmin):
    meta = Media
    list_display = ['name', 'tmdb_id', 'type']


class VideoAdmin(admin.ModelAdmin):
    meta = Video
    list_display = ['tmdb_id', 'name', 'media', 'location', 'type', 'popularity', 'release_date', 'rating']


class GenreAdmin(admin.ModelAdmin):
    meta = Genre
    list_display = ['name', 'tmdb_id', ]


class TVShowAdmin(admin.ModelAdmin):
    meta = Genre
    list_display = ['name', 'tmdb_id', ]


admin.site.register(Media, MediaAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(TVShow, TVShowAdmin)
