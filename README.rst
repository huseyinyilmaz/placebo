Placebo |build|_
================

Placebo is a utility that help mock api endpoints in a reusable and composable way.


Sample mock:

::

   class UsersResponse(BaseMock):
       url = 'http://www.acme.com/api/v1/users/'
       body = json.dumps([{'name': 'Huseyin',
                           'last_name': 'Yilmaz'}])

And usage of the mock will be like this:

::

   @Response.decorate
   def users_api_test(self):
       ...


You can decorate any function or method with this decorator. Even django views:

::

   @Response.decorate
   def users_list_view(request):
       ...

If your code is using multiple api endpoints you can easily stack responses on top of each other.

::

   @AuthResponse.decorate
   @Response.decorate
   def test_valid_get_user(request):
       ...

   @AuthResponse.decorate(status=401)
   @Response.decorate
   def test_cannot_authenticate(request):
       ...

   @AuthResponse.decorate
   @Response.decorate(status=503)
   def test_api_is_not_available(request):
       ...


For more information, please refer to documentation_


.. |build| image:: https://travis-ci.org/huseyinyilmaz/placebo.svg?branch=master
.. _build: https://travis-ci.org/huseyinyilmaz/placebo

.. _documentation: http://placebo.readthedocs.io/en/stable/
