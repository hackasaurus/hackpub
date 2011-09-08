This is a cross-origin RESTful API that allows Hackasaurus hacks to be shared.
It requires a front-end interface, which will be implemented in the
[Web X-Ray Goggles][]. [Mockups][] for the proposed interface are available.

The API uses Amazon S3 as a storage backend, so the API host doesn't need to
set up a database.

In the future, CAPTCHA support and other mechanisms can be added to the API
to deal with abuse.

  [Web X-Ray Goggles]: http://hackasaurus.org/goggles
  [Mockups]: http://www.flickr.com/photos/toolness/6127458033/in/photostream

# Quick Start

First, clone the repository and enter its directory:

    git clone git://github.com/hackasaurus/hackpub.git
    cd hackpub

Then copy `settings_local.sample.py` to `settings_local.py` and edit
it as necessary. Feel free to override any of the defaults set in
`settings.py` too.

Then, run the unit tests to make sure everything works:

    python manage.py test
    
You can also run S3 integration tests, which create a temporary bucket
on your S3 account and clean it up before exiting.

    python manage.py test_s3storage

Finally, start the development server:

    python manage.py runserver

By default, the development server hosts its cross-origin API to all
domains at http://127.0.0.1:8000/.

# Using the API

The API is quite simple.

## `POST /publish` ##

This method takes a body of type application/x-www-form-urlencoded
containing the following parameters:

* `html` - UTF-8 encoded HTML of the hack.
* `original-url` (optional) - The URL which the hack remixes.

If successful, the method returns `200 OK` with a JSON response
containing the following keys:

* `published-url` - The URL at which the hack can be viewed. The
  pathname component of the URL, excluding the first slash,
  is a short alphanumeric key uniquely identifying the hack.

If the hack is too big to store, this method can also return
`413 Request Entity Too Large`.

## `GET /metadata/<hack-key>` ##

This method returns `200 OK` with a JSON blob containing information about
the hack with the given key. It contains the following keys:

* `original-url` - The URL which the hack remixes.
* `published-url` - The URL where the hack is hosted.
* `created` - The date on which the hack was published, in
  IETF RFC 822/1123 format.
