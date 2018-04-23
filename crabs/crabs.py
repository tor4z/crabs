from queue import PriorityQueue, Empty
import re
from .route import Route
from .options import Travel, Method
from .logs import Log
from .handler import DefaultHandler
from .threadpool.threadpool import ThreadPoolExecutor
from .client.url import URL, URLError
from .client.utils import ClientHeaders
from .client.client import (Client, 
                            HttpError, 
                            ClientTooManyRedirects, 
                            HttpConnError)

class Crabs:
    def __init__(self):
        self._routes_ = None
        self._seed = []
        self._urls = PriorityQueue()
        self._travel_mod = Travel.BFS
        self._max_depth = 6
        self._allow_netlocs_re = []
        self._disallow_paths_re = []
        self._initialized = False
        self._log_name = self.__class__.__name__
        self._log_format = None
        self._log_level = None
        self._log_file = None
        self._log = None
        self._client = None
        self._executor = None
        self._scraped_count = 0
        self._max_redirects = None
        self._client_headers = {}
    
    @property
    def _routes(self):
        if self._routes_ is None:
            self._routes_ = Route()
        return self._routes_

    def update_client_headers(self, headers):
        if not isinstance(headers, dict):
            raise TypeError("Dict required.")
        self._client_headers.update(headers)

    def set_client_max_redirects(self, max_redirects):
        self._max_redirects = max_redirects

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

    def set_disallow_path(self, paths):
        if not isinstance(paths, list):
            raise TypeError("List required.")
        for path in paths:
            path = re.compile(re.sub(r"\*", "\w*" ,path))
            self._disallow_paths_re.append(path)

    def update_routes(self, routes):
        self._routes.update_routes(routes)

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

    def set_executor(self, max_size=None, queue_cls=None):
        self._executor = ThreadPoolExecutor._instance(max_size, 
                                                      queue_cls)

    def _new_url(self, url, origin=None, depth=0):
        return URL(url, origin, depth, self._travel_mod)

    def _init_seed(self):
        for url in self._seed:
            if not URL.is_full_url(url):
                raise URLError
            self.put_url(self._new_url(url))

    def _init_log(self):
        if self._log is None:
            self._log = Log(self._log_name, 
            self._log_format, self._log_level, self._log_file)

    def _init_default_client_headers(self):
        self.update_client_headers(ClientHeaders)
        
    @property
    def executor(self):
        if self._executor is None:
            self.set_executor()
        return self._executor
    
    @property
    def client(self):
        if self._client is None:
            self._client = Client(self._client_headers)
        return self._client

    @property
    def log(self):
        return self._log

    def initialize(self):
        if not self._initialized:
            self._init_seed()
            self._init_log()
            self._init_default_client_headers()
            self._initialized = True

    def _check_depth(self, url):
        return url.depth <= self._max_depth

    def _put_url(self, url):
        if not isinstance(url, URL):
            raise TypeError("URL required.")
        if self._check_depth(url) and self._url_filter(url):
            self._urls.put(url)

    def put_urls(self, urls):
        if urls:
            if not isinstance(urls, list):
                raise TypeError("List required.")
            for url in urls:
                self.put_link(url)

    def put_url(self, url):
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

    def _path_filter(self, url):
        if not self._disallow_paths_re:
            return True
        for path_re in self._disallow_paths_re:
            if path_re.match(url.path):
                return False
        return True

    def _url_filter(self, url):
        return self._netloc_filter(url) and\
               self._path_filter(url)

    def _put_urls_from_resp(self, resp):
        try:
            for url in resp.html.find_all_links():
                url = self._new_url(url, depth = resp.depth)
                self.put_url(url)
        except TypeError:
            pass

    def _exec_handler(self, handler):
        try:
            resp = handler.execute()
            self._put_urls_from_resp(resp)
            self._scraped_count += 1
        except HttpError as e:
            self.log.warning("HttpError({0}):{1}".format(e, handler.url))
        except ClientTooManyRedirects as e:
            self.log.warning(e)
        except HttpConnError as e:
            self.log.warning(e)

    def report(self):
        url_pool_size = self._urls.qsize()
        print("URL Pool Size: {0} - Scraped: {1} - Log: {2}".format(
            url_pool_size, self._scraped_count, self._log.statistics), end="\r")

    def _route_loop(self):
        while True:
            self.report()
            url = self._get_url(block=False)
            self.log.info("Scraping: {0}".format(url))
            handler_cls, url, method = self._routes.dispatch(url)
            if handler_cls is None:
                handler_cls = DefaultHandler
                method = Method.GET
            handler = handler_cls(url, method, self)
            self._exec_handler(handler)

    def run(self):
        try:
            self.initialize()
            self._route_loop()
        except KeyboardInterrupt:
            self.log.info("Exit.")
        except Empty:
            self.log.fatal("URL set empty.")

        self.shutdown()

    def shutdown(self, wait=True):
        if self._executor is not None:
            self._executor.shutdown(wait)