import traceback
from pathlib import Path
import hashlib
import yaml


def get_media_dirs(media_dir_stream):
    result = dict()
    movie_dir_map = dict()
    for media_location in media_dir_stream[0].replace('\n', '').replace('\r', '').split(','):
        movie_dir_map[hashlib.md5(media_location.encode('utf-8')).hexdigest()] = Path(media_location)

    tv_dir_map = dict()
    for tv_location in media_dir_stream[1].replace('\n', '').replace('\r', '').split(','):
        tv_dir_map[hashlib.md5(tv_location.encode('utf-8')).hexdigest()] = Path(tv_location)

    result['movie_dir_map'] = movie_dir_map
    result['tv_dir_map'] = tv_dir_map
    return result


class Config:
    __filepath = None
    __config = dict()
    __movie_dirs_map = dict()
    __tv_dirs_map = dict()

    def __init__(self, config_filepath=None):
        blank_config = {
            'movie_dir': list(),
            'tv_dir': list()
        }
        self.__filepath = config_filepath
        try:
            with open(self.__filepath) as f:
                self.__config = yaml.load(f, Loader=yaml.FullLoader)

            if (
                    (not self.__config) or
                    (type(self.__config) != dict) or
                    (type(self.__config.get('movie_dir')) != list) or
                    (type(self.__config.get('tv_dir')) != list)
            ):
                self.__config = blank_config
                try:
                    with open(self.__filepath, 'w') as f:
                        data = yaml.dump(self.__config, f)
                except Exception as ex:
                    print('Config :: update -> ', ex)
                    traceback.print_exc()

        except Exception as ex:
            self.__config = blank_config
            try:
                with open(self.__filepath, 'w') as f:
                    data = yaml.dump(self.__config, f)
            except Exception as ex:
                print('Config :: update -> ', ex)
                traceback.print_exc()
            print('Config::init: -> Creating a fresh config.yaml file')
        finally:

            if type(self.__config.get('movie_dir')) == list:
                for media_location in self.__config.get('movie_dir'):
                    self.__movie_dirs_map[hashlib.md5(media_location.encode('utf-8')).hexdigest()] = Path(
                        media_location)

            if type(self.__config.get('tv_dir')) == list:
                for tv_location in self.__config.get('tv_dir'):
                    self.__tv_dirs_map[hashlib.md5(tv_location.encode('utf-8')).hexdigest()] = Path(tv_location)

    def get(self):
        return self.__config

    def get_movie_dirs_map(self):
        return self.__movie_dirs_map

    def get_tv_dirs_map(self):
        return self.__tv_dirs_map

    def add_to_tv_dirs(self, new_tv_dir):
        if Path(new_tv_dir).exists() and (new_tv_dir not in self.__config['tv_dir']):
            self.__config['tv_dir'].append(new_tv_dir)
            self.__tv_dirs_map[hashlib.md5(new_tv_dir.encode('utf-8')).hexdigest()] = Path(new_tv_dir)

    def add_to_movie_dirs(self, new_movie_dir):
        if Path(new_movie_dir).exists() and (new_movie_dir not in self.__config['movie_dir']):
            self.__config['movie_dir'].append(new_movie_dir)
            self.__movie_dirs_map[hashlib.md5(new_movie_dir.encode('utf-8')).hexdigest()] = Path(new_movie_dir)

    def remove_from_movie_dirs(self, movie_dir):
        if self.__config['movie_dir'] and movie_dir in self.__config['movie_dir']:
            self.__config['movie_dir'].remove(movie_dir)
            del self.__movie_dirs_map[hashlib.md5(movie_dir.encode('utf-8')).hexdigest()]

    def remove_from_tv_dirs(self, tv_dir):
        if self.__config['tv_dir'] and tv_dir in self.__config['tv_dir']:
            self.__config['tv_dir'].remove(tv_dir)
            del self.__tv_dirs_map[hashlib.md5(tv_dir.encode('utf-8')).hexdigest()]

    def refresh(self):
        try:
            with open(self.__filepath) as f:
                self.__config = yaml.load(f, Loader=yaml.FullLoader)

            if type(self.__config.get('movie_dir')) == list:
                for media_location in self.__config.get('movie_dir'):
                    self.__movie_dirs_map[hashlib.md5(media_location.encode('utf-8')).hexdigest()] = Path(
                        media_location)

            if type(self.__config.get('tv_dir')) == list:
                for tv_location in self.__config.get('tv_dir'):
                    self.__tv_dirs_map[hashlib.md5(tv_location.encode('utf-8')).hexdigest()] = Path(tv_location)

        except Exception as ex:
            print('Config :: init -> ', ex)
            traceback.print_exc()

    def update(self, updated_config=None):
        if updated_config:
            self.__config = updated_config
        try:
            with open(self.__filepath, 'w') as f:
                data = yaml.dump(self.__config, f)
        except Exception as ex:
            print('Config :: update -> ', ex)
            traceback.print_exc()
