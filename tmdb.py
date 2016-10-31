import os
import requests

tmdb_api = os.environ.get('TMDB_API_KEY')

'''
The movie information need is:
1. Country
2. Year
3. Length
4. Director
5. Rating
6. Distributor
7. Language
'''


def search_tmdb(movie):
    url = 'https://api.themoviedb.org/3/search/movie'
    payload = {'api_key': tmdb_api, 'query': movie}
    r = requests.get(url, data=payload)
    results = r.json()['results']
    movie_id = results[0]['id']
    return movie_id


def get_details(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}'.format(movie_id)
    payload = {'api_key': tmdb_api}
    r = requests.get(url, data=payload)
    info = r.json()
    title = info['original_title']
    release = info['release_date']
    print(title)
    print(release)
    return title, release


def get_credits(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}/credits'.format(movie_id)
    payload = {'api_key': tmdb_api}
    r = requests.get(url, data=payload)
    crew = r.json()['crew']
    for i, member in enumerate(crew):
        if member['job'] == 'Director':
            director = member['name']
            break
    print(director)
    return director
