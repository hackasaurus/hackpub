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

def WSGIHandler():
    from hackpub.app import Application
    from hackpub.s3storage import S3Storage
    
    storage = S3Storage(
        access_key_id=settings.AWS_ACCESS_KEY_ID,
        secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        bucket=settings.BUCKET_NAME,
        publish_domain=settings.PUBLISH_DOMAIN
    )
    app = Application(settings=settings, storage=storage)
    return app

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

    from hackpub.test import test_app

    loader = unittest.defaultTestLoader
    suite = test_app.load_tests(loader, unittest.TestSuite(), args.pattern)
    unittest.TextTestRunner(verbosity=2).run(suite)

@command
def test_s3storage(args):
    'test S3Storage class against Amazon S3'

    import hackpub.test.test_s3storage

    hackpub.test.test_s3storage.run(settings)

if __name__ == '__main__':
    run()
