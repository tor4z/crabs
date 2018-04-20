from urllib.parse import urljoin, urlsplit
import re

class URL:
    def __init__(self, url, origin):
        if url is None or origin is None:
            raise TypeError
        if not isinstance(url, str):
            url = str(url)
        if not isinstance(origin, str):
            origin = str(origin)
        self._url = url
        self._origin = origin
        self._scheme = None
        self._netloc = None
        self._url_split_ = None
        self._depth = 0
        self._full_url_reobj = None

    def insc_depth(self):
        self._depth += 1

    def desc_depth(self):
        self._depth -= 1

    @property
    def depth(self):
        return self._depth

    def __lt__(self, other):
        return self.depth < other.depth
    
    def __gt__(self, other):
        return not self.__lt__(other)

    def __hash__(self):
        return self.url.__hash__()

    def __str__(self):
        return self.url

    def __repr__(self):
        return self.url

    @property
    def _is_full_url(self):
        if self._full_url_reobj is None:
            self._full_url_reobj = re.compile(r"\w+://.+")
        if self._full_url_reobj.match(self._url):
            return True
        else:
            return False

    @property
    def url(self):
        if not self._is_full_url:
            self._url = urljoin(self._origin, self._url)
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
    def scheme(self):
        if self._scheme is None:
            self._scheme = self._url_split.scheme
        return self._scheme