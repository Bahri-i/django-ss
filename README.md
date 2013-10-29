Saleor
======

Avast ye landlubbers! Saleor be a Satchless store ye can fork.

[![Build Status](https://travis-ci.org/mirumee/saleor.png?branch=master)](https://travis-ci.org/mirumee/saleor)


Usage
-----

1. Use `django-admin.py` to start a new project using Saleor as template:

   ```
   $ django-admin.py startproject \
   --template=https://github.com/mirumee/saleor/archive/master.zip myproject
   ```
2. Enter the directory:

   ```
   $ cd myproject/
   ```
3. Install it in development mode:

   ```
   $ python setup.py develop
   ```
   (For production use `python setup.py install` instead.)
4. Prepare the database:

   ```
   $ saleor syncdb --all
   ```

   `saleor` is a shortcut for running `python manage.py` so you can use it to execute all management commands.


Google Analytics
----------------

Because of EU law regulations, Saleor will not use any tracking cookies by default. We do support server-side Google Analytics out of the box using [Google Analytics Measurement Protocol](https://developers.google.com/analytics/devguides/collection/protocol/v1/). This is implemented using [google-measurement-protocol](https://pypi.python.org/pypi/google-measurement-protocol) and does not use cookies for the cost of not reporting things like geolocation and screen resolution. To get it working you will need to set the `GOOGLE_ANALYTICS_TRACKING_ID` in your settings file:

```python
# settings.py
GOOGLE_ANALYTICS_TRACKING_ID = 'UA-123456-78'
```


Testing changes
---------------

Run the tests to make sure everything works:

```
$ python setup.py test
```
