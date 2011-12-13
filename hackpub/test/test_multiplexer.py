import unittest

from webtest import TestApp
from webob.dec import wsgify
from webob import Response
from hackpub.multiplexer import Multiplexer

@wsgify
def sample_app_1(req):
    return Response('app_1:%s' % req.path_info)
    
@wsgify
def sample_app_2(req):
    return Response('app_2:%s' % req.path_info)

class MultiplexerTests(unittest.TestCase):
    def setUp(self):
        wsgiapp = Multiplexer(sample_app_1, 'more', {
            'two': sample_app_2
        })
        self.app = TestApp(wsgiapp)
        
    def test_multiplexer_works_for_default(self):
        res = self.app.get('/flarg')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.body, 'app_1:/flarg')

    def test_multiplexer_works_for_secondary(self):
        res = self.app.get('/more/two/flarg')
        self.assertEqual(res.status, '200 OK')
        self.assertEqual(res.body, 'app_2:/flarg')

    def test_multiplexer_404s(self):
        res = self.app.get('/more/three/', status=404)
        res = self.app.get('/more/two', status=404)
