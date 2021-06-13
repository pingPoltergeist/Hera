import requests
import json


class Tmdb:
    API_URL = 'https://api.themoviedb.org/3'
    API_KEY = 'adfff9c3b0688cc13ae8d7b0291b257e'

    MOVIE_API = '/movie'
    COLLECTION_API = '/collection'

    def call_api(self, api, parameter):
        url = '{api_url}/{api}/{parameter}?api_key={api_key}&language=en-US'.format(
            api_url=self.API_URL, api=api, parameter=parameter,  api_key=self.API_KEY)
        return requests.get(url).json()

    def validate_genre(self):
        a = self.API_KEY
        return False

