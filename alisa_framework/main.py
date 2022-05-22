from quopri import decodestring

from alisa_framework.requests import PostRequests, GetRequests


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


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

        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            post_request = PostRequests(environ)
            data = post_request.post_request_params()
            request['data'] = Framework.decode_value(data)
            print(f'POST-запрос: {Framework.decode_value(data)}')
        else:
            get_request = GetRequests(environ)
            data = get_request.get_request_params()
            request['data'] = Framework.decode_value(data)
            print(f'GET-параметры: {Framework.decode_value(data)}')

        for front in self.fronts_obj:
            front(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for key, value in data.items():
            val = bytes(value.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[key] = val_decode_str
        return new_data


