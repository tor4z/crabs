from crabs.handler import Handler
import re

class Route:
    _METHODS = ["GET", "POST"]
    _HANDLERS = []
    _PATTERNS = []
    _ROUTE = {
        "GET": [],
        "POST": []
    }

    @classmethod
    def _check_method(cls, method):
        if method in cls._METHODS:
            return True
        else:
            raise NotSupportMethodExp

    @classmethod
    def dispatch(cls, url, method="GET"):
        self._check_method(method)
        for pt, func in cls._ROUTE[method]:
            if pt.match(url):
                func(url) # TODO

    @classmethod
    def listen(cls, pattern, handler, method="GET"):
        if not isinstance(handler, Handler):
            raise TypeError
        self._check_method(method)
        cls._ROUTE[method].append(
            (re.compile(pattern), handler)
        )
        cls._HANDLERS.append(handler)
        cls._PATTERNS .append(handler)

    @classmethod
    def dispatch_url(cls, url):
        for handler in cls._HANDLERS:
            if handler.is_match(url):
                return handler.new_url(url)

class NotSupportMethodExp(Exception):
    pass