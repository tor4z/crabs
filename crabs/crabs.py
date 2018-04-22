from queue import PriorityQueue, Empty
from .url import URL, URLError
from .route import Route
from .options import Travel
from .client import ClientConnError
from .logs import Log
from .handler import HttpError
import re

class Crabs:
    def __init__(self):
        self._routes_ = None
        self._seed = []
        self._urls = PriorityQueue()
        self._travel_mod = Travel.BFS
        self._max_depth = 6
        self._allow_netlocs_re = []
        self._initialized = False
        self._log_name = self.__class__.__name__
        self._log_format = None
        self._log_level = None
        self._log_file = None
        self._log = None
        self._client_headers = {}
    
    @property
    def _routes(self):
        if self._routes_ is None:
            self._routes_ = Route()
        return self._routes_

    def set_client_headers(self, headers):
        if not isinstance(headers, dict):
            raise TypeError("Dict required.")
        self._client_headers.update(headers)

    def set_log_name(self, name):
        self._log_name = name
    
    def set_log_format(self, format):
        self._log_format = format
    
    def set_log_level(self, level):
        self._log_level = level

    def set_log_file(self, file):
        self._log_file = file

    def set_allow_netloc(self, netlocs):
        if not isinstance(netlocs, list):
            raise TypeError("List required.")
        for netloc in netlocs:
            netloc = re.compile(re.sub(r"\*", "\w*?" ,netloc))
            self._allow_netlocs_re.append(netloc)

    def set_routes(self, routes):
        self._routes.set_routes(routes)

    def set_max_depth(self, depth):
        if depth < 1:
            raise ValueError
        self._max_depth = depth
    
    def set_treval_mod(self, mod):
        if mod not in Travel.All:
            raise ValueError
        self._travel_mod = mod

    def set_seeds(self, seeds):
        if not isinstance(seeds, list):
            raise TypeError("List required.")
        self._seed = seeds

    def _new_url(self, url, origin=None, depth=0):
        return URL(url, origin, depth, self._travel_mod)

    def _init_seed(self):
        for url in self._seed:
            if not URL.is_full_url(url):
                raise URLError
            self.put_link(self._new_url(url))

    def _init_log(self):
        if self._log is None:
            self._log = Log(self._log_name, 
            self._log_format, self._log_level, self._log_file)
        
    @property
    def log(self):
        return self._log

    def initialize(self):
        if not self._initialized:
            self._init_seed()
            self._init_log()
            self._initialized = True

    def _check_depth(self, url):
        return url.depth <= self._max_depth

    def _put_url(self, url):
        if not isinstance(url, URL):
            raise TypeError("URL required.")
        if self._check_depth(url) and self._url_filter(url):
            self._urls.put(url)

    def put_links(self, urls):
        if urls:
            if not isinstance(urls, list):
                raise TypeError("List required.")
            for url in urls:
                self.put_link(url)

    def put_link(self, url):
        if isinstance(url, URL):
            pass
        elif isinstance(url, str):
            url = self._new_url(url)
        else:
            raise TypeError
        self._put_url(url)

    def _get_url(self, *args, **kwargs):
        return self._urls.get(*args, **kwargs)

    def _netloc_filter(self, url):
        if not self._allow_netlocs_re:
            return True
        for netloc_re in self._allow_netlocs_re:
            if netloc_re.match(url.netloc):
                return True
        return False

    def _url_filter(self, url):
        return self._netloc_filter(url)

    def _exec_handler(self, handler):
        try:
            handler.execute()
        except ClientConnError:
            self.log.exception("ClientConnError:{0}".format(handler.url))
        except HttpError as e:
            self.log.exception("HttpError(0):{1}".format(e, handler.url))

        urls = handler.links()
        for url, depth in urls:
            url = self._new_url(url, depth=depth)
            self.put_link(url)

    def _route_loop(self):
        while True:
            url = self._get_url(block=False)
            self.log.info("Scraping:{0}".format(url))
            handler = self._routes.dispatch(url)
            handler.set_headers(self._client_headers)
            self._exec_handler(handler)

    def run(self):
        try:
            self.initialize()
            self._route_loop()
        except KeyboardInterrupt:
            self.log.info("Exit.")
        except Empty:
            self.log.fatal("URL set empty.")