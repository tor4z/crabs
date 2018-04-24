from urllib.parse import urljoin, urlsplit, parse_qsl
import re
from .options import Travel

_FULL_URL_RE = re.compile(r"\w+://.+")

class URL:
    def __init__(self, url, path=None, depth=0, treval_mod=None):
        if url is None:
            raise TypeError
        if not isinstance(url, str):
            url = str(url)
        if path and not isinstance(path, str):
            path = str(path)
        self._url = url
        self._scheme = None
        self._netloc = None
        self._path = path
        self._url_split_ = None
        self._depth = depth
        self._query = None
        self._query_str = None
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

    def set_path(self, path):
        self._path = path

    def set_query(self, query):
        if not isinstance(query, dict):
            raise TypeError("Dict required.")
        self._query = query

    @property
    def raw(self):
        return self.urljoin(self._url, self.path_query)

    @property
    def _url_split(self):
        if self._url_split_ is None:
            self._url_split_ = urlsplit(self._url)
        return self._url_split_

    @property
    def netloc(self):
        if self._netloc is None:
            self._netloc = self._url_split.netloc
        return self._netloc

    @property
    def path_query(self):
        return self.path + "?" + self.query_str

    @property
    def query(self):
        if self._query is None:
            self._query = dict(parse_qsl(self.query_str))
        return self._query

    @staticmethod
    def dict_to_qs(qd):
        if not isinstance(qd, dict):
            raise TypeError("Dict required.")
        qs=""
        for key in qd:
            qs += "{0}={1}&".format(key, qd[key])
        return qs[:-1]
    
    @property
    def query_str(self):
        if self._query_str is None:
            if self._query is None:
                self._query_str = urlsplit(self.path).query
            else:
                self._query_str = self.dict_to_qs(self._query)
        return self._query_str

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

    @property
    def host(self):
        return urljoin(self._url, "/")

    @classmethod
    def urljoin(cls, url, path):
        if path is None:
            raise URLError
        if not cls.is_full_url(path):
            url = urljoin(url, path)
        else:
            url = path
        return url

class URLError(Exception):
    pass