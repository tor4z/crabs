import re

class Route:
    _METHODS = ["GET", "POST"]
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
                func(url)

    @classmethod
    def listen(cls, pattern, func, method="GET"):
        if not callable(func):
            raise TypeError
        self._check_method(method)
        cls._ROUTE[method].append(
            (re.compile(pattern), func)
        )

    @classmethod
    def start(cls):
        pass

class NotSupportMethodExp(Exception):
    pass