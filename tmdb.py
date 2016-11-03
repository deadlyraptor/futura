import os
import requests

tmdb_api = os.environ.get('TMDB_API_KEY')


class TMDB(object):
    def __init__(self):
        self.api = tmdb_api
        self.base_uri = 'https://api.themoviedb.org/3/'


class Search(TMDB):
    def search(self, movie):
        endpoint = 'search/movie'
        payload = {'api_key': self.api, 'query': movie}
        r = requests.get(self.base_uri + endpoint, data=payload)
        results = r.json()['results']
        first_three_movies = []
        for result in results[:3]:
            film = {}
            film['title'] = result['title']
            film['id'] = result['id']
            first_three_movies.append(film)
        return first_three_movies


class Movie(TMDB):
    def __init__(self, movie_id):
        super().__init__()
        self.movie_id = movie_id
        self.endpoints = {'details': 'movie/{}'.format(movie_id),
                          'credits': 'movie/{}/credits'.format(movie_id)}
        self.payload = {'api_key': self.api}

    def details(self):
        '''Returns the primary information about a movie.

        Contains the movie's country, year, length, and language.

        Arguments:
            none
        Returns:
            info = A dictionary.
        '''
        endpoint = self.endpoints['details']
        r = requests.get(self.base_uri + endpoint, data=self.payload)
        info = r.json()
        return info

    def credits(self):
        '''Returns the cast and crew information about a movie.

        Contains the director of the movie.

        Arguments:
            none
        Returns:
            cast = The cast of the movie.
            crew = The crew of the movie.
        '''
        endpoint = self.endpoints['credits']
        r = requests.get(self.base_uri + endpoint, data=self.payload)
        cast, crew = r.json()['cast'], r.json()['crew']
        return cast, crew
