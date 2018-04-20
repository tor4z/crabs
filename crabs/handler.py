import re

class Handler:
    def __init__(self):
        self._url_key_pattern = None
        self.init()
        self._check_pattern()

    def set_key_pattern(self, pattern):
        self._url_key_pattern = re.compile(pattern)

    @classmethod
    def is_match(cls, url):
        return self._url_key_pattern.match(url) is None

    def _check_pattern(self):
        if self._url_key_pattern is None:
            raise URLKeyPatternNotSetExp

    def get(self):
        raise NotImplemented

    def init(self):
        raise NotImplemented

class URLKeyPatternNotSetExp(Exception):
    pass