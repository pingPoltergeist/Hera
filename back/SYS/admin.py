from django.contrib import admin
from .models import System, MediaDirectory


# Register your models here.
class SystemAdmin(admin.ModelAdmin):
    meta = System
    list_display = ['key', 'value']


@admin.register(MediaDirectory)
class MediaDirectoryAdmin(admin.ModelAdmin):
    meta = MediaDirectory
    list_display = ['folder_location', 'folder_hash', 'movie_dir', 'movie_last_sync', 'tv_dir', 'tv_last_sync']


admin.site.register(System, SystemAdmin)
