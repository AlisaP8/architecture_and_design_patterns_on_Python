class PageNotFound404:
    def __call__(self, request):
        return '404 PAGE Not Found'


class Framework:
    def __init__(self, routes_obj, fronts_obj):
        self.routes_obj = routes_obj
        self.fronts_obj = fronts_obj

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        if not path.endswith('/'):
            path = f'{path}/'

        if path in self.routes_obj:
            view = self.routes_obj[path]
        else:
            view = PageNotFound404()
        request = {}

        for front in self.fronts_obj:
            front(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]


