from crabs.handler import Handler
from crabs.options import method
import re

class Route:
    _METHODS = [method.GET, method.POST]
    _HANDLERS = []
    _PATTERNS = []
    _ROUTE = {
        method.GET: [],
        method.POST: []
    }

    @classmethod
    def _check_method(cls, method):
        if method in cls._METHODS:
            return True
        else:
            raise NotSupportMethodExp

    @classmethod
    def dispatch(cls, url, method=method.GET):
        self._check_method(method)
        for pt, func in cls._ROUTE[method]:
            if pt.match(url):
                func(url) # TODO

    @classmethod
    def listen(cls, pattern, handler, method=method.GET):
        if not isinstance(handler, Handler):
            raise TypeError
        self._check_method(method)
        cls._ROUTE[method].append(
            (re.compile(pattern), handler)
        )
        cls._HANDLERS.append(handler)
        cls._PATTERNS.append(handler)

class NotSupportMethodExp(Exception):
    pass