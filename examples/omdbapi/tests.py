import mock
from unittest import TestCase
from api import get_movie
from testdata import GetMovieValidResponse


class RawAPITests(TestCase):

    @mock.patch('requests.get')
    def test_get_movie_with_valid_response(self, fake_get):
        fake_response = fake_get.return_value
        fake_response.ok = True
        fake_response.json.return_value = {
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
            'imdbVotes': '1,204,431'}

        movie = get_movie('matrix', 1999)
        self.assertEqual(movie,
                         {'director': 'Lana Wachowski, Lilly Wachowski',
                          'rated': 'R',
                          'language': 'English',
                          'title': 'The Matrix'})

    @mock.patch('requests.get')
    def test_get_movie_with_500_response(self, fake_get):
        fake_response = fake_get.return_value
        fake_response.ok = False
        fake_response.json.return_value = ''

        movie = get_movie('matrix', 1999)
        self.assertEqual(movie, None)


class omdbapiTests(TestCase):
    """Omdb api test cases"""

    expected_movie = {'director': 'Lana Wachowski, Lilly Wachowski',
                      'rated': 'R',
                      'language': 'English',
                      'title': 'The Matrix'}

    @GetMovieValidResponse.decorate
    def test_get_movie_valid_response(self):
        movie = get_movie('matrix', 1999)
        self.assertEqual(movie, GetMovieValidResponse.expected_api_response)

    @GetMovieValidResponse.decorate(status=500)
    def test_get_movie_500_response(self):
        movie = get_movie('matrix', 1999)
        self.assertEqual(movie, None)
