This is a cross-origin RESTful API that allows HTML or JSON to be published.
It requires a front-end interface, which is implemented in applications like 
the [Web X-Ray Goggles][] and [lovebomb.me][].

The API uses Amazon S3 as a storage backend, so the API host doesn't need to
set up a database.

In the future, CAPTCHA support and other mechanisms can be added to the API
to deal with abuse.

  [Web X-Ray Goggles]: http://hackasaurus.org/goggles
  [lovebomb.me]: https://github.com/toolness/lovebomb.me

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
containing one (but not both) of the following parameters:

* `html` - UTF-8 encoded HTML to publish.
* `json` - JSON-encoded data to publish.

Optionally, the following may also be supplied:

* `original-url` (optional) - The URL which the content remixes or is
  based on.

If successful, the method returns `200 OK` with a JSON response
containing the following keys:

* `published-url` - The URL at which the HTML or JSON can be viewed. The
  pathname component of the URL, excluding the first slash,
  is a short alphanumeric key uniquely identifying the content.

If the data is too big to store, this method can also return
`413 Request Entity Too Large`.

## `GET /metadata/<content-key>` ##

This method returns `200 OK` with a JSON blob containing information about
the content with the given key. It contains the following keys:

* `original-url` - The URL which the content remixes or is based on.
* `published-url` - The URL where the content is hosted.
* `created` - The date on which the content was published, in
  IETF RFC 822/1123 format.

# Sample Code

Here's sample jQuery code that submits some HTML to publish.

    jQuery.ajax({
      type: 'POST',
      url: 'http://example.org/publish',
      data: {
        'html': 'Hi, I am HTML!',
        'original-url': window.location.href
      },
      crossDomain: true,
      success: function(data) {
        console.log("HTML published to " + data['published-url']);
      }
    });
