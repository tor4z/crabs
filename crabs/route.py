import re
from .options import Method

class Route:
    def __init__(self):
        self._methods = [Method.GET, Method.POST]
        self._routes = []

    def _check_method(self, method):
        if method in self._methods:
            return True
        else:
            raise NotSupportMethodExp

    def update_routes(self, routes):
        if not isinstance(routes, list):
            raise TypeError("List required.")
        for route in routes:
            route_para_n = len(route)
            if route_para_n >= 2:
                self.regist(*route)
            else:
                raise RouteError            

    def dispatch(self, url):
        for pt, handler_cls, method in self._routes:
            if pt.match(url.raw):
                return handler_cls, url, method
        return None, url, None
        
    def _ext_pattern(self, pattern):
        return r".+" + pattern

    def regist(self, pattern, handler, method=Method.GET):
        self._check_method(method)
        self._routes.append(
            (re.compile(self._ext_pattern(pattern)), handler, method)
        )

class NotSupportMethodExp(Exception):
    pass

class RouteError(Exception):
    pass