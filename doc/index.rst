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

Consider following function:

.. code-block:: python

    def get_movie(title, year):
        """Sends a request to omdbapi to get movie data.

        If there is a problem with connection, returns None.
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

Let's think about how we could test this function. A classic way to test this code is
following:


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

This tests are fine. But they has two main disadvantages. First, code for mocking and actual function invocation is done in the same place which makes it hard to read. Second, if we keep writing similar tests we will probably copy the data for every test.

Purpose of placebo is to separate data from the actual tests. So It would be a lot easier to reason about. Placebo mocks will also be reusable and composable.

Here is how same code could be implemented with placebo:

First we create a placebo object for that endpoint.


.. code-block:: python

   class GetMovieValidResponse(Placebo):

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


After having all the data in place, we can use our placebo to decorate our test functions like this.

.. code-block:: python

   class omdbapiTests(TestCase):
       """Omdb api test cases"""
   
       @GetMovieValidResponse.decorate
       def test_get_movie_valid_response(self):
           movie = get_movie('matrix', 1999)
           self.assertEqual(movie, GetMovieValidResponse.expected_api_response)
   
       @GetMovieValidResponse.decorate(status=500)
       def test_get_movie_500_response(self):
           movie = get_movie('matrix', 1999)
           self.assertEqual(movie, None)


In first method, we directly used the placebo object. In the second method we changed the status of the object to 500 and tested the error case. Notice how logic for mocking the endpoint and test is seperated. We also reused same object for testing the valid response and error case.

As a matter of fact, placebo object is not only usefull for testing. Since main interface is a decorator pattern,  you can use it on any function you want, like views in your web application. That way you can develop your applicarions against mock data or simulate error cases on your development environment very easily.


Installation
============

Placebo can be installed using pip

.. code-block:: bash

   $ pip install python-placebo

Or source code can be downloaded from github.

Basic Usage
===========

Basic usage of placebo can be following

.. code-block:: python

   class SimplePlacebo(Placebo):
       url = 'http://www.acme.com/items/'
       body = '[{"id": 1}, {"id": 2}, {"id": 3}]'

When we decorate a function with this placebo class, every 'GET' request to http://www.acme.com/items/ url will return 200 response with following body '[{"id": 1}, {"id": 2}, {"id": 3}]'.

We can use this placebo in following test:

.. code-block:: python

   @SimplePlacebo.decorate
   def test_get_list_valid(self):
       api = ItemAPIClient()
       result = api.get_items()
       self.assertEqual(result,
                        [{"id": 1}, {"id": 2}, {"id": 3}])

Defaut value for status code is 200 and default value for http method is 'GET'. So we did not need to specify those values in our class. If we wanted to specify all fields, we could do something like this:

.. code-block:: python

   class SimplePlaceboWithAllFields(Placebo):
       url = 'http://www.acme.com/items/'
       body = '[{"id": 1}, {"id": 2}, {"id": 3}]'
       status = 200
       method = 'GET'
       headers = {'custom-header': 'custom'}


In placebo class, "url, body, status, method, headers attributes" can be used to define the mock request. method and url is used to figure out which requests should be mocked. Requests that does not match with given url and methods will go to real backend. "body, status, headers" attributes are used as matching request's content.

There are 2 different ways those attributes can be specified. First, by adding them to Placebo class. Second is update them on decorator. Following tests updates already defined class with diffent status and body.

.. code-block:: python

    @SimplePlacebo.decorate(status=500)
    def test_get_list_error(self):
        api = ItemAPIClient()
        with self.assertRaises(ItemException):
            api.get_items()

     @SimplePlacebo.decorate(body='invalid-body')
    def test_get_list_invalid_body_error(self):
        api = ItemAPIClient()
        with self.assertRaises(ItemException):
            api.get_items()

Impementing Placebo classes
===========================

Static placebo classes
----------------------
A placebo class can have following properties.

.. code-block:: python

   class SimplePlaceboWithAllFields(Placebo):
       url = 'http://www.acme.com/items/'
       method = 'GET'
       body = '[{"id": 1}, {"id": 2}, {"id": 3}]'
       status = 200
       headers = {'custom-header': 'custom'}

       backend = httprettybackend.get_decorator

1) *url*:  Url that will be matched to decide if placebo mock is applied. It can be a string, urlparse.ParseResult or urlparse.SplitResult.

2) *method*: HTTP method that will be matched to decide if placebo mock is applied. It should be a string like GET, POST, PUT, DELETE. Default value for method is GET.

3) *body*: If mock object is applied body will be used as response body. It should be type of string.

4) *status*: If mock object is applied status will be used as http status code of response. It should be an integer like 200, 404 or 500. Default value for status is 200.

5) *headers*: If mock is applied headers will be used as http headers. type of headers should be a dictionary. (Keys should be header names and values should be header values.)

6) *backend*: Backends provides actual functionality of placebo. Currently there are two different backends are supported by default. httpretty and httmock. By default httmock is tried if it cannot be imported httpretty is tried. backend is basically a function that gets a placebo object as argument and mocks the current apis.

Dynamic placebo classes
-----------------------

Previous pacebo class has static properties width already defined values. Most of the properties of placebo object can also be defined as methods therefore values can be calculated on the fly. Here is an example placebo objects that returns a mock response with id it receives. If id is not an integer, it returns 404 response. Even though those kind of placebo objects are not suitable for tests, they are very usefull for development.


.. code-block:: python

   class DynamicPlacebo(Placebo):

       backend = httmockbackend

       url_regex = re.compile('^http://www.acme.com/items/(?P<item_id>\d+)/$')
   
       def url(self):
           return parse.ParseResult(
               scheme='http',
               netloc=r'www\.acme\.com',
               path=r'^/items/(\w+)/$',
               params='',
               query='',
               fragment='')
   
       def method(self):
           return 'GET'
   
       def body(self, request_url, request_headers, request_body):
           url = request_url.geturl()
           regex_result = self.url_regex.match(url)
           if regex_result:
               item_id = int(regex_result.groupdict()['item_id'])
               return json.dumps({'id': int(item_id)})
           else:
               return ''
   
       def headers(self, request_url, request_headers, request_body):
           return {}
   
       def status(self, request_url, request_headers, request_body):
           """If item_id is not integer return 404."""
   
           url = request_url.geturl()
           regex_result = self.url_regex.match(url)
           # if item_id is not a number return 404
           if regex_result:
               status = 200
           else:
               status = 404
           return status

As seen in the example, almost all the properties of Placebo object can be written as methods. Some properties are evaluated for each request therefore receives url, headers, body. Rest of the properties are evaluated only once on initialization therefore does not receive any extra information about the request. Only property that cannot be implemented as method is backend. The reason for that is backend has a type of function so we cannot distinguish backends from methods that returns backends.
