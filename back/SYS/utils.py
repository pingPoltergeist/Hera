import datetime
import json
import os
import pathlib
import re
import traceback
from pathlib import Path
from django.conf import settings
from CORE.models import Media, Video, Genre, TVShow
from SYS.models import MediaDirectory
from Hera.apis import TMDB, Fanart


def matcher(season_no: int, name, matching_type):
    match = lambda x: re.search(x, str(name), re.IGNORECASE)
    matching_type = matching_type.lower()
    return bool(
        (matching_type.lower() == 'movie' and bool(match('(\\D|^){}(\\D|$)'.format(str(season_no).zfill(2))))) or
        (matching_type.lower() == 'movie' and bool(match('(\\D|^){}(\\D|$)'.format(str(season_no))))) or
        bool(match(r'{type}\s*{season_no}(\D|$)'.format(type=matching_type[0], season_no=str(season_no)))) or
        bool(match(r'{type}\s*{season_no}(\D|$)'.format(type=matching_type[0], season_no=str(season_no).zfill(2)))) or
        bool(match(r'{type}\s*{season_no}(\D|$)'.format(type=matching_type, season_no=str(season_no)))) or
        bool(match(r'{type}\s*{season_no}(\D|$)'.format(type=matching_type, season_no=str(season_no).zfill(2))))
    )


def get_dir_files_stat(directory=None, media_dir_hash=None):
    file_date = dict()
    try:
        os.chdir(directory)
        media_dir = MediaDirectory.objects.filter(folder_hash=media_dir_hash).first()
        for file in os.listdir():
            if file and (os.path.splitext(file)[1] in ['.mp4', '.mpeg4', '.webm', '.mkv', '.wmv', '.avi']):
                modify_time = datetime.datetime.fromtimestamp(os.path.getmtime(pathlib.Path(file))).astimezone()
                create_time = datetime.datetime.fromtimestamp(os.path.getctime(pathlib.Path(file))).astimezone()
                is_sync = (
                        media_dir
                        and media_dir.last_sync
                        and modify_time < media_dir.last_sync
                        and create_time < media_dir.last_sync
                )
                file_date[file] = {
                    'media_dir_hash': media_dir_hash,
                    'create_time': create_time,
                    'is_sync': is_sync
                }
    except Exception as e:
        traceback.print_exc()
    return file_date


def get_all_movie_file_stat():
    stat = dict()
    for media_dir_hash, directory in settings.MOVIES_DIRS_MAP.items():
        stat.update(get_dir_files_stat(directory, media_dir_hash))
    return stat


def get_dir_tv_shows_stat(directory=None, media_dir_hash=None):
    file_date = dict()
    try:
        directory and os.chdir(directory)
        for file in [name for name in os.listdir() if os.path.isdir(os.path.join(name))]:
            modify_time = datetime.datetime.fromtimestamp(os.path.getmtime(pathlib.Path(file))).astimezone()
            create_time = datetime.datetime.fromtimestamp(os.path.getctime(pathlib.Path(file))).astimezone()
            media_dir = MediaDirectory.objects.filter(folder_hash=media_dir_hash).first()
            is_sync = (
                    media_dir
                    and media_dir.last_sync
                    and modify_time < media_dir.last_sync
                    and create_time < media_dir.last_sync
            )
            file_date[file] = {
                'create_time': create_time,
                'location': str(pathlib.Path(file).absolute()),
                'media_dir_hash': media_dir_hash,
                'is_sync': is_sync,
            }
    except Exception as e:
        traceback.print_exc()
    return file_date


def get_all_tv_show_file_stat():
    stat = dict()
    for media_dir_hash, directory in settings.TVSHOWS_DIRS_MAP.items():
        stat.update(get_dir_tv_shows_stat(directory, media_dir_hash))
    return stat


def get_genre_array(genre_ids=None):
    tmdb = TMDB()
    all_genres = None
    if genre_ids:
        genres = []
        for linked_genre in genre_ids:
            genre_id = linked_genre['id']
            if Genre.objects.filter(tmdb_id=genre_id):
                genres.append(Genre.objects.get(tmdb_id=genre_id))
            else:
                try:
                    if not all_genres:
                        all_genres = tmdb.get_all_genre()
                    if all_genres.get(genre_id):
                        genre = Genre.objects.create(
                            tmdb_id=genre_id,
                            name=all_genres[genre_id]
                        )
                        genre.save()
                        genres.append(genre)
                except Exception as e:
                    traceback.print_exc()
        return genres


def add_tv_show_to_db(tmdb_data, tv_files_data: dict, media_dir: MediaDirectory):
    tv_show_folder_name = list(tv_files_data.keys())[0]
    tv_shows = None
    tmdb = TMDB()
    fanart = Fanart()
    try:
        tv_shows, status = TVShow.objects.get_or_create(
            tmdb_id=tmdb_data.get('id'),
            media_dir=media_dir,
        )
        tv_shows.name = tmdb_data.get('name')
        tv_shows.description = tmdb_data.get('overview')
        tv_shows.type = 'T'
        tv_shows.local_path = tv_show_folder_name
        tv_shows.rating = tmdb_data.get('vote_average')
        tv_shows.popularity = tmdb_data.get('popularity')
        tv_shows.tagline = tmdb_data.get('tagline')

        if tmdb_data.get('poster_path'):
            tv_shows.poster_image = TMDB.TMDB_IMAGE_URL + tmdb_data.get('poster_path')
        if tmdb_data.get('backdrop_path'):
            tv_shows.background_image = TMDB.TMDB_IMAGE_URL + tmdb_data.get('backdrop_path')
        if tmdb_data['genres']:
            tv_shows.genre.add(*get_genre_array(tmdb_data['genres']))

        if tmdb_data['seasons']:
            tv_shows.season_count = len(tmdb_data['seasons'])
            tv_shows.release_date = datetime.datetime.strptime(tmdb_data['seasons'][0]['air_date'], '%Y-%m-%d').date()

        logo_and_thumbnail = fanart.get_logo_and_thumbnail(tmdb_data.get('id'), 'tv')
        if logo_and_thumbnail:
            tv_shows.logo = logo_and_thumbnail.get('logo')
            tv_shows.thumbnail = logo_and_thumbnail.get('thumbnail')

        trailer = tmdb.get_trailer(tmdb_data.get('id'), 'tv')
        if trailer:
            tv_shows.trailer = trailer

        if tmdb_data.get('episode_run_time'):
            tv_shows.episode_runtime = datetime.timedelta(
                minutes=int(tmdb_data.get('episode_run_time')[0])
            ) if type(tmdb_data.get('episode_run_time')[0]) is int else None

        if tmdb_data['seasons']:
            # location and os.chdir(location)
            available_seasons_dirs_data: dict = tv_files_data[tv_show_folder_name]
            for season in tmdb_data['seasons']:
                if not season.get('season_number'):
                    continue
                print(f"===========================season_number: {season.get('season_number')}===========================")
                for available_seasons_dir_name, available_files_in_seasons_dir in available_seasons_dirs_data.items():
                    print(f"\t{available_seasons_dir_name} | "
                          f"{matcher(season.get('season_number'), available_seasons_dir_name, 'season')}"
                          f"---------------------")
                    if matcher(season.get('season_number'), available_seasons_dir_name, 'season'):
                        episodes = tmdb.get_episode_by_tv_show_id(tmdb_data['id'], season.get('season_number'))
                        for episode in episodes:
                            print(f"\t\t episode: {episode.get('episode_number')}")
                            for available_file in available_files_in_seasons_dir:
                                print(f"\t\t episode: {episode.get('episode_number')} | {available_file} | {matcher(episode.get('episode_number'), available_file, 'episode')}")
                                if matcher(episode.get('episode_number'), available_file, 'episode'):
                                    episode_added = tv_shows.add_episode_from_episode_data(
                                        episode=episode,
                                        location='/media{media_hash}/{show}/{season}/{episode}'.format(
                                            media_hash=media_dir.folder_hash,
                                            show=tv_show_folder_name,
                                            season=available_seasons_dir_name,
                                            episode=available_file
                                        )
                                    )
                                    if episode_added:
                                        available_files_in_seasons_dir.remove(available_file)
        if tv_shows.video_set.count():
            tv_shows.save()
        else:
            tv_shows.delete()
        return True
    except Exception:
        if tv_shows:
            tv_shows.delete()
        traceback.print_exc()
        return False


def add_movie_to_db(tmdb_data, filename, media_dir: MediaDirectory):
    location = '/media{id}/{filename}'.format(id=media_dir.folder_hash, filename=filename),
    if Video.objects.filter(tmdb_id=tmdb_data['id']):
        video = Video.objects.get(tmdb_id=tmdb_data['id'])
        video.location = location
        video.save()
        return True
    video = None
    media = None
    tmdbapi = TMDB()
    fanartapi = Fanart()
    try:
        video = Video.objects.create(
            tmdb_id=tmdb_data.get('id'),
            name=tmdb_data.get('original_title'),
            description=tmdb_data.get('overview'),
            location=location,
            type='M',
            rating=tmdb_data.get('vote_average'),
            added_at=datetime.datetime.now(),
            popularity=tmdb_data.get('popularity'),
            tagline=tmdb_data.get('tagline'),
            media_dir=media_dir
        )
        if tmdb_data.get('poster_path'):
            video.poster_image = TMDB.TMDB_IMAGE_URL + tmdb_data.get('poster_path')
        if tmdb_data.get('backdrop_path'):
            video.background_image = TMDB.TMDB_IMAGE_URL + tmdb_data.get('backdrop_path')

        video.duration = datetime.timedelta(minutes=int(tmdb_data.get('runtime'))) if type(
            tmdb_data.get('runtime')) is int else None

        logo_and_thumbnail = fanartapi.get_logo_and_thumbnail(tmdb_data.get('id'), 'movie')
        if logo_and_thumbnail:
            video.logo = logo_and_thumbnail.get('logo')
            video.thumbnail = logo_and_thumbnail.get('thumbnail')

        trailer = tmdbapi.get_trailer(tmdb_data.get('id'), 'movie')
        if trailer:
            video.trailer = trailer

        try:
            video.release_date = datetime.datetime.strptime(tmdb_data.get('release_date'), '%Y-%m-%d').date()
        except Exception as ex:
            traceback.print_exc()

        if tmdb_data['genres']:
            video.genre.add(*get_genre_array(tmdb_data['genres']))

        if tmdb_data['belongs_to_collection']:
            if Media.objects.filter(tmdb_id=tmdb_data['belongs_to_collection']['id']):
                media = Media.objects.get(tmdb_id=tmdb_data['belongs_to_collection']['id'])
            else:
                collection = tmdbapi.get_collection_by_id(tmdb_data['belongs_to_collection']['id'])

                media = Media.objects.create(
                    tmdb_id=collection.get('id'),
                    name=collection.get('name').replace('Collection', '').strip(),
                    description=collection.get('overview'),
                    type='M',
                    is_collection=True,
                    media_dir=media_dir
                )
                if collection.get('backdrop_path'):
                    media.background_image = TMDB.TMDB_IMAGE_URL + collection.get('backdrop_path')

                if collection.get('poster_path'):
                    media.poster_image = TMDB.TMDB_IMAGE_URL + collection.get('poster_path')

            media.save()
            video.media = media

        video.save()
        return True
    except Exception as e:
        if video:
            video.delete()
        if media and not media.video_set.all():
            media.delete()
        traceback.print_exc()
        return False
