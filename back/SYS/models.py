import os
import traceback
from django.db import models
from pathlib import Path
import datetime


# Create your models here.
class System(models.Model):
    key = models.CharField(primary_key=True, max_length=1000)
    value = models.CharField(max_length=1000, blank=True, null=True)


class MediaDirectory(models.Model):
    folder_location = models.CharField(max_length=1000)
    folder_hash = models.CharField(max_length=100, unique=True)

    movie_dir = models.BooleanField(default=False)
    movie_last_sync = models.DateTimeField(null=True, blank=True)

    tv_dir = models.BooleanField(default=False)
    tv_last_sync = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '{} [{}]'.format(self.folder_location, self.folder_hash)

    def get_non_synced_movie_files(self):
        res = list()
        if not self.movie_dir:
            return res
        location = Path(self.folder_location)
        for file in os.listdir(location):
            if file and (os.path.splitext(file)[1] in ['.mp4', '.mpeg4', '.webm', '.mkv', '.wmv', '.avi']):
                # print(self, 'line 46')
                if not self.movie_sync_status_of_file(location / file):
                    res.append(file)
        return res

    def get_non_synced_tv_shows(self):
        res = dict()
        if not self.tv_dir:
            return res
        location = Path(self.folder_location)
        try:
            for folder_name in [name for name in os.listdir(location) if os.path.isdir(location / name)]:
                folder_list = dict()
                folder = location / folder_name
                for sub_folder_name in [name for name in os.listdir(folder) if os.path.isdir(folder / name)]:
                    sub_folder_list = list()
                    sub_folder = folder / sub_folder_name
                    try:
                        for file in os.listdir(sub_folder):
                            if file and (
                                    os.path.splitext(file)[1] in ['.mp4', '.mpeg4', '.webm', '.mkv', '.wmv', '.avi']):
                                if not self.tv_sync_status_of_file(sub_folder / file):
                                    sub_folder_list.append(file)
                        if sub_folder_list:
                            folder_list.update({sub_folder_name: sub_folder_list})
                    except Exception:
                        traceback.print_exc()
                if folder_list:
                    res.update({folder_name: folder_list})
        except Exception as e:
            print(e)
            traceback.print_exc()
        return res

    def movie_sync_status_of_file(self, file_path: Path):
        modify_time = datetime.datetime.fromtimestamp(os.path.getmtime(Path(file_path))).astimezone()
        create_time = datetime.datetime.fromtimestamp(os.path.getctime(Path(file_path))).astimezone()
        return (
                self.movie_last_sync
                and modify_time < self.movie_last_sync
                and create_time < self.movie_last_sync
        )

    def tv_sync_status_of_file(self, file_path: Path):
        modify_time = datetime.datetime.fromtimestamp(os.path.getmtime(Path(file_path))).astimezone()
        create_time = datetime.datetime.fromtimestamp(os.path.getctime(Path(file_path))).astimezone()
        return (
                self.tv_last_sync
                and modify_time < self.tv_last_sync
                and create_time < self.tv_last_sync
        )

    @staticmethod
    def update_media_directory(movie_dirs, tv_dirs):
        for movieDirectory in MediaDirectory.objects.filter(movie_dir=True):
            if movieDirectory.folder_hash not in movie_dirs.keys():
                # print('MediaDirectory::update_media_directory:removing Movie flag -> ', movieDirectory)
                movieDirectory.movie_dir = False
                movieDirectory.save()
        for tvDirectory in MediaDirectory.objects.filter(tv_dir=True):
            if tvDirectory.folder_hash not in tv_dirs.keys():
                # print('MediaDirectory::update_media_directory:removing TV flag -> ', tvDirectory)
                tvDirectory.tv_dir = False
                tvDirectory.save()

        deleted = MediaDirectory.objects.filter(movie_dir=False, tv_dir=False).delete()
        # print('MediaDirectory::update_media_directory:deleted files -> ', deleted)

        movie_dir_list = list()
        for movie_dir_hash, movie_dir in movie_dirs.items():
            movie_dir_qs, status = MediaDirectory.objects.get_or_create(
                folder_location=str(movie_dir),
                folder_hash=movie_dir_hash
            )
            movie_dir_qs.movie_dir = True
            movie_dir_qs.save()

            movie_dir_list.append({
                'folder_location': movie_dir_qs.folder_location,
                'folder_hash': movie_dir_qs.folder_hash,
                'folder_type': 'MOVIE',
                'last_sync': movie_dir_qs.movie_last_sync,
            })

        tv_dir_list = list()
        for tv_dir_hash, tv_dir in tv_dirs.items():
            tv_dir_qs, status = MediaDirectory.objects.get_or_create(
                folder_location=str(tv_dir),
                folder_hash=tv_dir_hash
            )
            tv_dir_qs.tv_dir = True
            tv_dir_qs.save()

            tv_dir_list.append({
                'folder_location': tv_dir_qs.folder_location,
                'folder_hash': tv_dir_qs.folder_hash,
                'folder_type': 'TV',
                'last_sync': tv_dir_qs.tv_last_sync,
            })
        return {
            'movie_dirs': movie_dir_list,
            'tv_dirs': tv_dir_list
        }
