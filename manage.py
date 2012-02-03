import os
import site

ROOT = os.path.abspath(os.path.dirname(__file__))
path = lambda *x: os.path.join(ROOT, *x)

site.addsitedir(path('vendor'))
site.addsitedir(path('.'))

from ezcommandline import arg, command, run

try:
    import settings_local as settings
except ImportError:
    import settings

def make_storage(settings):
    from hackpub.s3storage import S3Storage
    
    return S3Storage(
        access_key_id=settings.AWS_ACCESS_KEY_ID,
        secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        bucket=settings.BUCKET_NAME,
        publish_domain=settings.PUBLISH_DOMAIN
    )

def BaseWSGIHandler(settings):
    from hackpub.app import Application

    app = Application(settings=settings, storage=make_storage(settings))
    return app

def WSGIHandler():
    from hackpub.multiplexer import Multiplexer
    
    primary_app = BaseWSGIHandler(settings)
    extra_buckets = {}
    for bucket in settings.EXTRA_BUCKETS:
        extra_settings = settings.EXTRA_BUCKETS[bucket]
        extra_buckets[bucket] = BaseWSGIHandler(extra_settings)
    return Multiplexer(primary_app, 'buckets', extra_buckets)

@arg('--port', help='port to serve on', type=int, default=8000)
@command
def runserver(args):
    'run development server'

    from wsgiref.simple_server import make_server

    httpd = make_server('', args.port, WSGIHandler())
    print 'serving on port %s' % args.port
    httpd.serve_forever()

@arg('-p', '--pattern', help='test name pattern to match', default=None)
@command
def test(args):
    'run tests'
    
    import unittest

    from hackpub.test import test_app, test_multiplexer

    loader = unittest.defaultTestLoader
    suite = test_app.load_tests(loader, unittest.TestSuite(), args.pattern)
    suite.addTest(loader.loadTestsFromModule(test_multiplexer))
    unittest.TextTestRunner(verbosity=1).run(suite)

@command
def test_s3storage(args):
    'test S3Storage class against Amazon S3'

    import hackpub.test.test_s3storage

    hackpub.test.test_s3storage.run(settings)

@arg('-o', '--output-filename', help='filename to output to',
     default='extract.json')
@command
def extract(args):
    'Export all published work metadata as JSON'
    
    import pickle
    import json

    entries = {}
    cache_filename = settings.BUCKET_NAME + '.cache'
    if os.path.exists(cache_filename):
        cache = open(cache_filename, 'rb')
        eof = False
        while not eof:
            try:
                key, entry = pickle.load(cache)
                entries[key] = entry
            except EOFError:
                eof = True
        cache.close()

    cache = open(cache_filename, 'ab')
    storage = make_storage(settings)
    for entry in storage:
        if entry.key not in entries:
            metadata = storage.get_metadata(entry.key)
            entries[entry.key] = {
                'created': metadata.get('created'),
                'original-url': metadata.get('original-url'),
                'published-url': metadata.get('published-url'),
                'size': entry.size
            }
            pickle.dump([entry.key, entries[entry.key]], cache)
            print "added %s" % entry.key
    cache.close()

    outfile = open(args.output_filename, 'w')
    json.dump(entries, outfile)
    outfile.close()
    
    print "wrote %s." % args.output_filename

if __name__ == '__main__':
    run()
