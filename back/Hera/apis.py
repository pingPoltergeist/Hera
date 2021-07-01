import requests


class TMDB:
    TMDB_API_KEY = 'adfff9c3b0688cc13ae8d7b0291b257e'
    TMDB_URL = 'https://api.themoviedb.org/3'
    TMDB_IMAGE_URL = 'https://image.tmdb.org/t/p/original'
    TMDB_EXTRAS = '?api_key={api_key}&language=en-US'.format(api_key=TMDB_API_KEY)

    def search_movie(self, search_key=None):
        search_url = self.TMDB_URL + '/search/movie' + self.TMDB_EXTRAS \
                     + "&query={search_key}&page=1&include_adult=false".format(search_key=search_key)
        response = requests.get(search_url)
        return response

    def search_tv(self, search_key=None):
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
        response = requests.get(collection_url)
        return response.json()

    def get_all_genre(self):
        genre_url = self.TMDB_URL + '/genre/movie/list' + self.TMDB_EXTRAS
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
class Fanart:
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
            tmdb = TMDB()
            external_ids = tmdb.get_external_ids(tmdb_id=tmdb_id, media_type=media_type)
            media_id = external_ids.get('tvdb_id')
            media_url_type = media_type.lower()
        logo_and_thumbnail_url = self.FANART_URL + '/{media_type}/{id}'.format(
            media_type=media_url_type,
            id=media_id
        ) + self.FANART_EXTRAS
        response = requests.get(logo_and_thumbnail_url)
        data = response.json()
        if data.get('{media_type}logo'.format(media_type=media_type)):
            for logo in data['{media_type}logo'.format(media_type=media_type)]:
                if logo.get('lang') == 'en':
                    res['logo'] = logo['url']
                    break
            if not res['logo']:
                res['logo'] = data['{media_type}logo'.format(media_type=media_type)][0]['url']
        elif data.get('hd{media_type}logo'.format(media_type=media_type)):
            for logo in data['hd{media_type}logo'.format(media_type=media_type)]:
                if logo['lang'] == 'en':
                    res['logo'] = logo['url']
                    break
            if not res.get('logo'):
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
