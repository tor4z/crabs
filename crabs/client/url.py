from urllib.parse import urljoin, urlsplit
import re
from .options import Travel

_FULL_URL_RE = re.compile(r"\w+://.+")

class URL:
    def __init__(self, url, origin=None, depth=0, treval_mod=None):
        if url is None:
            raise TypeError
        if not isinstance(url, str):
            url = str(url)
        if origin and not isinstance(origin, str):
            origin = str(origin)
        self._url = url
        self._origin = origin or url
        self._scheme = None
        self._netloc = None
        self._path = None
        self._url_split_ = None
        self._depth = depth
        self._travel_mod = treval_mod or Travel.BFS
        self._full_url_reobj = None

    def insc_depth(self):
        self._depth += 1

    def desc_depth(self):
        self._depth -= 1

    @property
    def depth(self):
        return self._depth
    
    def _lt(self, other):
        if self._travel_mod == Travel.BFS:
            return self.depth < other.depth
        elif self._travel_mod == Travel.DFS:
            return self.depth > other.depth
        else:
            raise ValueError

    def __lt__(self, other):
        return self._lt(other)
    
    def __gt__(self, other):
        return not self._lt(other)

    def __hash__(self):
        return self.raw.__hash__()

    def __str__(self):
        return self.raw

    def __repr__(self):
        return self.raw

    @staticmethod
    def is_full_url(url):
        if _FULL_URL_RE.match(url):
            return True
        else:
            return False

    @property
    def raw(self):
        self._url = self.urljoin(self._origin, self._url)
        return self._url

    @property
    def _url_split(self):
        if self._url_split_ is None:
            self._url_split_ = urlsplit(self._origin)
        return self._url_split_

    @property
    def netloc(self):
        if self._netloc is None:
            self._netloc = self._url_split.netloc
        return self._netloc

    @property
    def path(self):
        if self._path is None:
            self._path = self._url_split.path
        return self._path

    @property
    def scheme(self):
        if self._scheme is None:
            self._scheme = self._url_split.scheme
        return self._scheme

    @classmethod
    def urljoin(cls, origin, url):
        if url is None:
            raise URLError
        if not cls.is_full_url(url):
            url = urljoin(origin, url)
        return url

class URLError(Exception):
    pass