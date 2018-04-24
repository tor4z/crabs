import re
from queue import PriorityQueue, Empty
from .http_client.url import URL
from .options import Travel, Method

class URLPool:
    def __init__(self):
        self._urls = PriorityQueue()
        self._travel_mod = Travel.BFS
        self._max_depth = 6
        self._allow_netlocs_re = []
        self._disallow_paths_re = []

    @property
    def size(self):
        return self._urls.qsize()

    def set_allow_netloc(self, netlocs):
        if netlocs is not None:
            if not isinstance(netlocs, list):
                raise TypeError("List required.")
            for netloc in netlocs:
                netloc = re.compile(re.sub(r"\*", "\w*?" ,netloc))
                self._allow_netlocs_re.append(netloc)

    def set_disallow_path(self, paths):
        if paths is not None:
            if not isinstance(paths, list):
                raise TypeError("List required.")
            for path in paths:
                path = re.compile(re.sub(r"\*", "\w*" ,path))
                self._disallow_paths_re.append(path)

    def set_treval_mod(self, mod):
        if mod is not None:
            if mod not in Travel.All:
                raise ValueError("Invalid travel mod.")
            self._travel_mod = mod

    def set_max_depth(self, depth):
        if depth is not None:
            if depth < 1:
                raise ValueError("Depth should be greater than 0.")
            self._max_depth = depth

    def new_url(self, url, path=None, depth=0):
        return URL(url, path, depth, self._travel_mod)

    def put_urls(self, urls):
        if not isinstance(urls, list):
            raise TypeError("List required.")
        for url in urls:
            self.put_url(url)

    def put_url(self, url):
        if isinstance(url, URL):
            if not self._check_depth(url) or not self._url_filter(url):
                return
        elif isinstance(url, str):
            url = self.new_url(url)
        else:
            raise TypeError
        self._urls.put(url)

    def get_url(self, *args, **kwargs):
        try:
            return self._urls.get(*args, **kwargs)
        except:
            raise URLPoolEmpty

    def _check_depth(self, url):
        return url.depth <= self._max_depth

    def _path_filter(self, url):
        if not self._disallow_paths_re:
            return True
        for path_re in self._disallow_paths_re:
            if path_re.match(url.path):
                return False
        return True

    def _netloc_filter(self, url):
        if not self._allow_netlocs_re:
            return True
        for netloc_re in self._allow_netlocs_re:
            if netloc_re.match(url.netloc):
                return True
        return False

    def _url_filter(self, url):
        return self._netloc_filter(url) and\
               self._path_filter(url)

class URLPoolEmpty(Exception):
    pass