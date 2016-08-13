Placebo |build|_
================

Placebo is a utility that help mock api endpoints in a reusable and composable way.


To use placebo first we should create a placebo class for our mock. Placebo class represents a response for certain request. If url and http method of any request matches with mock, response that is described in placebo class will be return. We can create a placebo mock like this:

::

   from placebo import Placebo

   class UsersResponse(Placebo):
       url = 'http://www.acme.com/api/v1/users/'
       body = json.dumps([{'name': 'Huseyin',
                           'last_name': 'Yilmaz'}])

Main interface for a placebo object is a decorator. Any function that decorated with a placebo class will be mocked with that placebo class.

::

   @UserResponse.decorate
   def users_api_test(self):
       ...


You can decorate any function or method with this decorator. Even django views! This makes development against external apis very easy.

::

   @UserResponse.decorate
   def users_list_view(request):
       ...

If your code is using multiple api endpoints you can easily stack placebo decorators on top of each other.

::

   @AuthResponse.decorate
   @UserResponse.decorate
   def test_valid_get_user(request):
       ...

   @AuthResponse.decorate(status=401)
   @UserResponse.decorate
   def test_cannot_authenticate(request):
       ...

   @AuthResponse.decorate
   @UserResponse.decorate(status=503)
   def test_api_is_not_available(request):
       ...


For more information, please refer to documentation_


.. |build| image:: https://travis-ci.org/huseyinyilmaz/placebo.svg?branch=master
.. _build: https://travis-ci.org/huseyinyilmaz/placebo

.. _documentation: http://placebo.readthedocs.io/en/stable/
