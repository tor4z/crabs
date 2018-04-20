from queue import PriorityQueue
from crabs.url import URL, URLError

class Crabs:
    _ROUTE = None
    _SEEDS = []
    _URLS = PriorityQueue()
    _INITIALIZED = False

    @classmethod
    def set_route(cls, route):
        cls._ROUTE = route

    @classmethod
    def set_seeds(cls, seeds):
        if not isinstance(seeds, list):
            raise TypeError("List required.")
        cls._SEEDS = seeds

    @classmethod
    def _init_seed(cls):
        for url in cls._SEEDS:
            if not URL.is_full_url(url):
                raise URLError
            cls._URLS.put(URL(url))

    @classmethod
    def initialize(cls):
        if not cls._INITIALIZED:
            cls._init_seed()
            cls._INITIALIZED = True

    @classmethod
    def put_links(cls, urls):
        if not isinstance(urls, list):
            urls = [urls]
        for url in urls:
            if isinstance(url, URL):
                cls._URLS.put(url)
            elif isinstance(url, str):
                cls._URLS.put(URL(url))
            else:
                raise TypeError

    @classmethod
    def _route_run(cls):
        pass

    @classmethod
    def run(cls):
        cls.initialize()
