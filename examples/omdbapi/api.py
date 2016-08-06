import requests


def get_movie(title, year):
    """Sends a request to omdbapi to get movie data.

    If there is a problem with connection returns None.
    """
    url = 'http://www.omdbapi.com/'

    params = {'t': title,
              'y': year,
              'plot': 'short',
              'r': 'json'}
    response = requests.get(url, params=params)
    if not response.ok:
        return None
    resp = response.json()
    return {
        'language': resp['Language'],
        'director': resp['Director'],
        'rated': resp['Rated'],
        'title': resp['Title']}
