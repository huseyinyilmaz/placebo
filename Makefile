test: test-httmock test-httpretty

test-httpretty:
	PLACEBO_BACKEND=placebo.backends.httprettybackend.get_decorator python setup.py test

test-httmock:
	PLACEBO_BACKEND=placebo.backends.httmockbackend.get_decorator python setup.py test

virtualenv3:
	mkvirtualenv placebo3 --python=`which python3`
