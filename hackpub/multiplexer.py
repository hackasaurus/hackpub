from wsgiref.util import shift_path_info

def Multiplexer(default_app, multiplex_dir, multiplex_apps):
    def app(environ, start_response):
        parts = environ['PATH_INFO'].split('/')[1:]
        if len(parts) >= 2 and parts[0] == multiplex_dir:
            app = multiplex_apps.get(parts[1])
            if len(parts) > 2 and app:
                shift_path_info(environ)
                shift_path_info(environ)
                return app(environ, start_response)
            else:
                start_response('404 Not Found',
                               [('Content-Type', 'text/plain')])
                return ['Not Found']
        return default_app(environ, start_response)

    return app
