import datetime
import json
import os
import pathlib
import re
import traceback

import requests
from django.conf import settings
from CORE.models import Media, Video, Genre, TVShow

last_sync = datetime.datetime(2021, 5, 12)


def matcher(season_no: int, name, matching_type):
    match = lambda x: re.search(x, str(name), re.IGNORECASE)
    matching_type = matching_type.lower()
    return bool(
        (matching_type.lower() == 'movie' and bool(match('(\\D|^){}(\\D|$)'.format(str(season_no).zfill(2))))) or
        (matching_type.lower() == 'movie' and bool(match('(\\D|^){}(\\D|$)'.format(str(season_no))))) or
        bool(match('{type}\\s*{season_no}(\\D|$)'.format(type=matching_type[0], season_no=str(season_no)))) or
        bool(match('{type}\\s*{season_no}(\\D|$)'.format(type=matching_type[0], season_no=str(season_no).zfill(2)))) or
        bool(match('{type}\\s*{season_no}(\\D|$)'.format(type=matching_type, season_no=str(season_no)))) or
        bool(match('{type}\\s*{season_no}(\\D|$)'.format(type=matching_type, season_no=str(season_no).zfill(2))))
    )


class TMDBAPI:
    TMDB_API_KEY = 'adfff9c3b0688cc13ae8d7b0291b257e'
    TMDB_URL = 'https://api.themoviedb.org/3'
    TMDB_IMAGE_URL = 'https://image.tmdb.org/t/p/original'
    TMDB_EXTRAS = '?api_key={api_key}&language=en-US'.format(api_key=TMDB_API_KEY)

    def search_movie(self, search_key=None):
        # print('---------', search_key)
        search_url = self.TMDB_URL + '/search/movie' + self.TMDB_EXTRAS \
                     + "&query={search_key}&page=1&include_adult=false".format(search_key=search_key)
        response = requests.get(search_url)
        return response

    def search_tv(self, search_key=None):
        # print('---------', search_key)
        search_url = self.TMDB_URL + '/search/tv' + self.TMDB_EXTRAS \
                     + "&query={search_key}&page=1&include_adult=false".format(search_key=search_key)
        response = requests.get(search_url)
        return response

    def get_movie_by_id(self, movie_id):
        movie_url = self.TMDB_URL + '/movie/{movie_id}'.format(movie_id=movie_id) + self.TMDB_EXTRAS
        response = requests.get(movie_url)
        return response.json()

    def get_tv_show_by_id(self, tv_id):
        tv_url = self.TMDB_URL + '/tv/{tv_id}'.format(tv_id=tv_id) + self.TMDB_EXTRAS
        response = requests.get(tv_url)
        return response.json()

    def get_episode_by_tv_show_id(self, tv_id, season_id):
        tv_url = self.TMDB_URL + '/tv/{tv_id}/season/{season_id}'.format(
            tv_id=tv_id,
            season_id=season_id
        ) + self.TMDB_EXTRAS
        response = requests.get(tv_url)
        return response.json().get('episodes')

    def get_collection_by_id(self, collection_id):
        collection_url = self.TMDB_URL + '/collection/{collection_id}'.format(
            collection_id=collection_id) + self.TMDB_EXTRAS
        # print(collection_id, type(collection_id), ' | ', collection_url)
        response = requests.get(collection_url)
        return response.json()

    def get_all_genre(self):
        genre_url = self.TMDB_URL + '/genre/movie/list' + self.TMDB_EXTRAS
        # print(genre_url)
        response = requests.get(genre_url)
        genres = dict()
        for genre in response.json().get('genres'):
            genres[genre['id']] = genre['name']
        return genres

    def get_trailer(self, tmdb_id, media_type=None):

        trailer_url = self.TMDB_URL + '/{media_type}/{tmdb_id}/videos'.format(
            media_type=media_type.lower(),
            tmdb_id=tmdb_id
        ) + self.TMDB_EXTRAS
        # print(trailer_url)
        response = requests.get(trailer_url)
        data = response.json()['results']
        trailer = None
        for video in data:
            if video.get('type') == "Trailer":
                return 'https://www.youtube.com/watch?v=' + video.get('key')
        return None

    # https://api.themoviedb.org/3/tv/71912/external_ids?api_key=adfff9c3b0688cc13ae8d7b0291b257e&language=en-US
    def get_external_ids(self, tmdb_id, media_type=None):
        external_ids_url = self.TMDB_URL + '/{media_type}/{tmdb_id}/external_ids'.format(
            media_type=media_type.lower(),
            tmdb_id=tmdb_id
        ) + self.TMDB_EXTRAS
        return requests.get(external_ids_url).json()


# https://webservice.fanart.tv/v3/movies/673?api_key=0a07e4f6e89f662683254b31e370bedb
class FanartAPI:
    FANART_API_KEY = '0a07e4f6e89f662683254b31e370bedb'
    FANART_URL = 'https://webservice.fanart.tv/v3'
    FANART_EXTRAS = '?api_key={api_key}'.format(api_key=FANART_API_KEY)

    def get_logo_and_thumbnail(self, tmdb_id, media_type=None):
        media_url_type = None
        res = dict()
        media_id = None
        if 'movie' in media_type.lower():
            media_id = tmdb_id
            media_url_type = 'movies'
        elif 'tv' in media_type.lower():
            tmdbapi = TMDBAPI()
            external_ids = tmdbapi.get_external_ids(tmdb_id=tmdb_id, media_type=media_type)
            media_id = external_ids.get('tvdb_id')
            media_url_type = media_type.lower()
        logo_and_thumbnail_url = self.FANART_URL + '/{media_type}/{id}'.format(
            media_type=media_url_type,
            id=media_id
        ) + self.FANART_EXTRAS
        response = requests.get(logo_and_thumbnail_url)
        # print(tmdb_id, ' | ', logo_and_thumbnail_url)
        data = response.json()
        # print("line: 183", data)
        if data.get('{media_type}logo'.format(media_type=media_type)):
            for logo in data['{media_type}logo'.format(media_type=media_type)]:
                if logo['lang'] == 'en':
                    res['logo'] = logo['url']
                    break
            if not res['logo']:
                res['logo'] = data['{media_type}logo'.format(media_type=media_type)][0]['url']
        elif data.get('hd{media_type}logo'.format(media_type=media_type)):
            for logo in data['hd{media_type}logo'.format(media_type=media_type)]:
                if logo['lang'] == 'en':
                    res['logo'] = logo['url']
                    break
            if not res['logo']:
                res['logo'] = data['hd{media_type}logo'.format(media_type=media_type)][0]['url']
        else:
            res['logo'] = None

        if data.get('{media_type}thumb'.format(media_type=media_type)):
            for logo in data['{media_type}thumb'.format(media_type=media_type)]:
                if logo['lang'] == 'en':
                    res['thumbnail'] = logo['url']
                    break
            if not res['logo']:
                res['thumbnail'] = data['{media_type}thumb'.format(media_type=media_type)][0]['url']
        else:
            res['thumbnail'] = None

        return res


def get_dir_files_stat(directory=None, media_dir_hash=None):
    file_date = dict()
    try:
        os.chdir(directory)
        for file in os.listdir():
            if file and (os.path.splitext(file)[1] in ['.mp4', '.mpeg4', '.webm', '.mkv', '.wmv', '.avi']):
                create_time = datetime.datetime.fromtimestamp(pathlib.Path(file).stat().st_mtime)
                is_sync = create_time < last_sync
                file_date[file] = {
                    'media_dir_hash': media_dir_hash,
                    'create_time': create_time,
                    'is_sync': is_sync
                }
    except Exception as e:
        print(e)
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
            create_time = datetime.datetime.fromtimestamp(pathlib.Path(file).stat().st_mtime)
            is_sync = create_time < last_sync
            file_date[file] = {
                'create_time': create_time,
                'location': str(pathlib.Path(file).absolute()),
                'media_dir_hash': media_dir_hash,
                'is_sync_with_db': is_sync,
            }
    except Exception as e:
        print(e)
        traceback.print_exc()
    return file_date


def get_all_tv_show_file_stat():
    stat = dict()
    for media_dir_hash, directory in settings.TVSHOWS_DIRS_MAP.items():
        stat.update(get_dir_tv_shows_stat(directory, media_dir_hash))
    return stat


def get_genre_array(genre_ids=None):
    tmdbapi = TMDBAPI()
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
                        all_genres = tmdbapi.get_all_genre()
                    if all_genres.get(genre_id):
                        genre = Genre.objects.create(
                            tmdb_id=genre_id,
                            name=all_genres[genre_id]
                        )
                        genre.save()
                        # print('adding Genre: {', genre, ' }', 'on line: 228')
                        genres.append(genre)
                except Exception as e:
                    print(e)
                    traceback.print_exc()
        return genres


def add_tv_show_to_db(tmdb_data, location=None, media_dir_hash=None):
    # if TVShow.objects.filter(tmdb_id=tmdb_data['id']):
    #     return True
    tv_shows = None
    tmdbapi = TMDBAPI()
    fanartapi = FanartAPI()
    try:
        tv_shows = TVShow.objects.get_or_create(
            tmdb_id=tmdb_data.get('id'),
        )[0]
        tv_shows.name = tmdb_data.get('name')
        tv_shows.description = tmdb_data.get('overview')
        tv_shows.type = 'T'
        tv_shows.local_path = location
        tv_shows.rating = tmdb_data.get('vote_average')
        tv_shows.popularity = tmdb_data.get('popularity')
        tv_shows.tagline = tmdb_data.get('tagline')

        if tmdb_data.get('poster_path'):
            tv_shows.poster_image = TMDBAPI.TMDB_IMAGE_URL + tmdb_data.get('poster_path')
        if tmdb_data.get('backdrop_path'):
            tv_shows.background_image = TMDBAPI.TMDB_IMAGE_URL + tmdb_data.get('backdrop_path')
        if tmdb_data['genres']:
            tv_shows.genre.add(*get_genre_array(tmdb_data['genres']))

        if tmdb_data['seasons']:
            tv_shows.season_count = len(tmdb_data['seasons'])
            tv_shows.release_date = datetime.datetime.strptime(tmdb_data['seasons'][0]['air_date'], '%Y-%m-%d').date()

        logo_and_thumbnail = fanartapi.get_logo_and_thumbnail(tmdb_data.get('id'), 'tv')
        if logo_and_thumbnail:
            tv_shows.logo = logo_and_thumbnail.get('logo')
            tv_shows.thumbnail = logo_and_thumbnail.get('thumbnail')

        trailer = tmdbapi.get_trailer(tmdb_data.get('id'), 'tv')
        if trailer:
            tv_shows.trailer = trailer

        if tmdb_data.get('episode_run_time'):
            tv_shows.episode_runtime = datetime.timedelta(
                minutes=int(tmdb_data.get('episode_run_time')[0])
            ) if type(tmdb_data.get('episode_run_time')[0]) is int else None

        if tmdb_data['seasons'] and location:
            # location and os.chdir(location)
            available_seasons_dirs = [name for name in os.listdir(location)
                                      if os.path.isdir(os.path.join(location, name))]
            for season in tmdb_data['seasons']:
                if not season.get('season_number'):
                    continue

                for available_seasons_dir in available_seasons_dirs:
                    if matcher(season.get('season_number'), available_seasons_dir, 'season'):
                        available_files = get_dir_files_stat(os.path.join(location, available_seasons_dir))
                        episodes = tmdbapi.get_episode_by_tv_show_id(tmdb_data['id'], season.get('season_number'))
                        for episode in episodes:
                            synced_file = None
                            for available_file, stat in available_files.items():
                                if matcher(episode.get('episode_number'), available_file, 'episode'):
                                    episode_video = None
                                    try:
                                        episode_video = tv_shows.video_set.get_or_create(tmdb_id=episode['id'])[0]
                                        episode_video.name = episode['name']
                                        episode_video.description = episode['overview']
                                        episode_video.rating = episode['vote_average']
                                        episode_video.season_no = episode['season_number']
                                        episode_video.type = 'T'
                                        episode_video.location = '/media{media_hash}/{show}/{season}/{episode}'.format(
                                            media_hash=media_dir_hash,
                                            show=location.split('\\')[-1],
                                            season=available_seasons_dir,
                                            episode=available_file
                                        )

                                        if episode['still_path']:
                                            episode_video.thumbnail = TMDBAPI.TMDB_IMAGE_URL + episode['still_path']
                                        episode_video.save()
                                        synced_file = available_file
                                    except Exception as ex:
                                        if episode_video:
                                            episode_video.delete()
                                        print(ex)
                                        traceback.print_exc()

                            if synced_file:
                                del available_files[synced_file]
        if tv_shows.video_set.count():
            tv_shows.save()
        else:
            tv_shows.delete()
        return True
    except Exception as e:
        print('Ex--------------', e, 'on TvShow: ', tv_shows.tmdb_id, '\n', json.dumps(tmdb_data))
        if tv_shows:
            tv_shows.delete()
        traceback.print_exc()
        return False


def add_movie_to_db(tmdb_data, location):
    if Video.objects.filter(tmdb_id=tmdb_data['id']):
        video = Video.objects.get(tmdb_id=tmdb_data['id'])
        video.location = location
        video.save()
        return True
    video = None
    media = None
    tmdbapi = TMDBAPI()
    fanartapi = FanartAPI()
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
        )
        if tmdb_data.get('poster_path'):
            video.poster_image = TMDBAPI.TMDB_IMAGE_URL + tmdb_data.get('poster_path')
        if tmdb_data.get('backdrop_path'):
            video.background_image = TMDBAPI.TMDB_IMAGE_URL + tmdb_data.get('backdrop_path')

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
            print(ex)
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

                )
                if collection.get('backdrop_path'):
                    media.background_image = TMDBAPI.TMDB_IMAGE_URL + collection.get('backdrop_path')

                if collection.get('poster_path'):
                    media.poster_image = TMDBAPI.TMDB_IMAGE_URL + collection.get('poster_path')

            media.save()
            # print('----------------------', media)
            video.media = media

        video.save()
        return True
    except Exception as e:
        if video:
            video.delete()
        if media and not media.video_set.all():
            media.delete()
        print('Ex--------------', e)
        traceback.print_exc()
        return False
