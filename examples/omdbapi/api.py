import requests


def get_movie(title, year):
    """
    Sends a request to omdbapi to get movie data.
    """
    url = 'http://www.omdbapi.com/'

    params = {'t': title,
              'y': year,
              'plot': 'short',
              'r': 'json'}
    response = requests.get(url, params=params)
    return response.json()
