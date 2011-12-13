import re
import time
from wsgiref.handlers import format_date_time

import simplejson
from webob.dec import wsgify
from webob import Response

METADATA_RE = re.compile(r'\/metadata\/([0-9a-zA-Z]+)')

class Application(object):
    def __init__(self, settings, storage, now=time.time):
        self.settings = settings
        self.storage = storage
        self.now = now

    def _response(self, content=None, status='200 OK'):
        if content is None:
            content = status
        if isinstance(content, unicode):
            content = str(content)
        if not isinstance(content, str):
            content = simplejson.dumps(content)
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        headers = [
            ('Content-Type', mimetype),
            ('Access-Control-Allow-Origin', self.settings.ALLOW_ORIGINS),
            # A custom header that jQuery ajax requests seem to contain.
            ('Access-Control-Allow-Headers', 'x-requested-with'),
            ('Access-Control-Allow-Methods', 'OPTIONS, GET, POST'),
        ]
        return Response(content, headerlist=headers, status=status)

    @wsgify
    def __call__(self, req):
        if req.method == 'OPTIONS':
            return self._response('')
        elif req.method == 'GET':
            if req.path == '/robots.txt':
                return self._response('User-agent: *\r\nDisallow: /\r\n')
            else:
                match = METADATA_RE.match(req.path_info)
                if match:
                    key = match.group(1)
                    metadata = self.storage.get_metadata(key)
                    if metadata is not None:
                        return self._response(metadata)
        elif req.method == 'POST' and req.path_info == '/publish':
            if not req.content_length:
                return self._response(status='411 Length Required')
            if req.content_length > self.settings.MAX_PAYLOAD_SIZE:
                return self._response(status='413 Request Entity Too Large')
            if 'html' not in req.POST or not req.POST['html'].strip():
                return self._response('Expected HTML.',
                                      status='400 Bad Request')
            html = req.POST['html']
            metadata = {
                'created': format_date_time(self.now())
            }
            if isinstance(html, unicode):
                html = html.encode('utf-8')
            if 'original-url' in req.POST:
                metadata['original-url'] = req.POST['original-url']
            url = self.storage.create(
                content=html,
                mimetype='text/html; charset=utf-8',
                metadata=metadata
            )
            return self._response({'published-url': url})
        else:
            return self._response(status='405 Method Not Allowed')

        return self._response('not found: %s' % req.path, status='404 Not Found')
