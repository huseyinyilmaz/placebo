import json
from placebo import Placebo


class GetMovieValidResponse(Placebo):

    # mock related data. That will be used in tests.
    title = 'matrix'
    year = 1999

    url = 'http://www.omdbapi.com/'
    body = json.dumps({
        'Actors': 'Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving',  # noqa
        'Awards': 'Won 4 Oscars. Another 33 wins & 44 nominations.',
        'Country': 'USA',
        'Director': 'Lana Wachowski, Lilly Wachowski',
        'Genre': 'Action, Sci-Fi',
        'Language': 'English',
        'Metascore': '73',
        'Plot': 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',  # noqa
        'Poster': 'http://ia.media-imdb.com/images/M/MV5BMTkxNDYxOTA4M15BMl5BanBnXkFtZTgwNTk0NzQxMTE@._V1_SX300.jpg',  # noqa
        'Rated': 'R',
        'Released': '31 Mar 1999',
        'Response': 'True',
        'Runtime': '136 min',
        'Title': 'The Matrix',
        'Type': 'movie',
        'Writer': 'Lilly Wachowski, Lana Wachowski',
        'Year': '1999',
        'imdbID': 'tt0133093',
        'imdbRating': '8.7',
        'imdbVotes': '1,204,431'})

    expected_api_response = {'director': 'Lana Wachowski, Lilly Wachowski',
                             'rated': 'R',
                             'language': 'English',
                             'title': 'The Matrix'}
