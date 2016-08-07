.. Placebo documentation master file, created by
   sphinx-quickstart on Wed Aug  3 23:50:37 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Placebo's documentation!
===================================

Introduction
============

Placebo is a tool for mocking external API's in python applications. It uses httmock or httpretty as mocking backend.


Why this is useful
------------------

Lets think about testing following function.

.. code-block:: python

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

To test this client, we could write following test case:

.. code-block:: python

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

This is a classic example of api client testing. It has two main disadvantages. First, code for mocking and actual function invocation is done in the same place which makes it hard to read. Second, if we keep writing similar tests we will probably copy the data for every test.

Here is how same code could be implemented with placebo:

First we create a placebo object for that endpoint.


.. code-block:: python

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


After having all the data in place we can use our placebo class to decorate our test functions like this. In first method, we directly used the placebo object. In the second method we changed the status of the object to 500 and tested the error case. Notice how logic for mocking the endpoint and test is seperated.

.. code-block:: python

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


As a matter of fact, placebo object is not only usefull for testing. You can add the decorator your views and develop your application against your test data.

INSTALLATION
============

placebo can be installed using pip

.. code-block:: bash

   $ pip install python-placebo

Or source code can be downloaded from github.

USAGE
=====

Basic usage of placebo can be following
